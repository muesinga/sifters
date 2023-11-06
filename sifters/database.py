import math


class Database:

    def __init__(self, mediator):

        self.connection = mediator.connection

        self.cursor = mediator.cursor

        self.grids_set = mediator.grids_set

        self.repeats = mediator.repeats

        self.period = mediator.period

        self.ticks_per_beat = mediator.ticks_per_beat

        self.scaling_factor = mediator.scaling_factor

        self.create_textures_table()

        self.create_notes_table()

        self.create_messages_table()

    
    def create_textures_table(self):
        sql_command = f'''
        CREATE TABLE IF NOT EXISTS textures (
            texture_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )'''
        self.cursor.execute(sql_command)
        self.connection.commit()


    def create_notes_table(self):
        sql_command = '''
        CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY,
            texture_id INTEGER,
            Start INTEGER,
            Velocity INTEGER,
            Note TEXT,
            Duration INTEGER,
            FOREIGN KEY (texture_id) REFERENCES textures(texture_id)
        )'''
        self.cursor.execute(sql_command)
        self.connection.commit()


    def create_messages_table(self):
        sql_command = '''
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY,
            note_id INTEGER,
            texture_id INTEGER,
            Start INTEGER,
            End INTEGER,
            Velocity INTEGER,
            Note INTEGER,
            Pitch INTEGER,
            Message TEXT,
            time INTEGER,
            FOREIGN KEY (note_id) REFERENCES notes(note_id),
            FOREIGN KEY (texture_id) REFERENCES textures(texture_id)
        )'''
        self.cursor.execute(sql_command)
        self.connection.commit()


    def find_first_texture_id(self, texture):
        sql_query = f'SELECT texture_id FROM "{texture}" LIMIT 1' # Define the SQL query to retrieve the first texture_id value.
        self.cursor.execute(sql_query) # Execute the SQL query.
        result = self.cursor.fetchone() # Fetch the result (should be a single row with the first texture_id).

        return result[0]  # Extract the first texture_id value from the result
    

    def fetch_distinct_texture_ids(self):
        self.cursor.execute("SELECT DISTINCT texture_id FROM notes")

        return [row[0] for row in self.cursor.fetchall()]
        

    def fetch_columns_by_table_name(self, table_name, exclude_columns={}):
        # Get the first row for the given table_name
        self.cursor.execute(f'SELECT * FROM "{table_name}"')
        row = self.cursor.fetchone()
        # Use the keys of the row (which are column names) and filter out the ones in the exclude set
        columns = [col for col in row.keys() if col not in exclude_columns]

        # return ', '.join(columns)
        return columns
    

    def generate_union_all_statements(self, texture_id, columns_string, duration_value, length_of_one_rep, repeat):
        accumulative_value = 0
        select_statements = []

        for _ in range(repeat):
            select_statements.append(f'''
            SELECT {columns_string}, 
            "Start" * {duration_value} + {accumulative_value} AS "Start",
            "Duration" * {duration_value} AS "Duration"
            FROM notes WHERE texture_id = {texture_id}''')
            accumulative_value += length_of_one_rep

        return " UNION ALL ".join(select_statements)
    

    def generate_sql_for_duration_values(self, texture_id, columns_list):
        columns_string = ', '.join(columns_list)
        duration_values = [grid * self.scaling_factor for grid in self.grids_set]
        length_of_reps = [int(math.pow(self.period, 2) * duration) for duration in duration_values]

        table_commands = {}
        for duration_value, length_of_one_rep, repeat in zip(duration_values, length_of_reps, self.repeats):
            table_name = f"texture_{texture_id}_{duration_value}"
            table_commands[table_name] = self.generate_union_all_statements(texture_id, columns_string, duration_value, length_of_one_rep, repeat)

        return table_commands
        

    def insert_into_notes_command(self, table_names):
        commands = []

        for table_name in table_names:
            cols = self.fetch_columns_by_table_name(table_name)
            cols_string = ', '.join([f'"{col}"' for col in cols])

            # Insert data from each table into the notes table
            sql_command = f'INSERT INTO notes ({cols_string}) SELECT {cols_string} FROM "{table_name}";'
            commands.append(sql_command)

        return "\n".join(commands)


    def generate_grouped_command(self, texture_id, columns):
        group_query_parts = [f'GROUP_CONCAT("{column}") as "{column}"' for column in columns]
        group_query_body = ', '.join(group_query_parts)
        return f'''
        CREATE TEMPORARY TABLE "texture_{texture_id}_grouped" AS
        SELECT Start, {group_query_body}
        FROM "Notes"
        WHERE texture_id = {texture_id}
        GROUP BY Start;
        '''


    def generate_max_duration_command(self, texture_id):
        return f'''
        CREATE TEMPORARY TABLE "texture_{texture_id}_max_duration" AS
        WITH max_durations AS (
            SELECT Start, MAX(Duration) as MaxDuration
            FROM "Notes"
            WHERE texture_id = {texture_id}
            GROUP BY Start
        )
        SELECT DISTINCT c.Start, c.Velocity, c.Note, m.MaxDuration as Duration
        FROM "Notes" c
        LEFT JOIN max_durations m ON c.Start = m.Start
        WHERE c.texture_id = {texture_id};
        '''
    
    def generate_create_and_insert_end_data_commands(self, texture_id):
        create_table_command = f'''
        CREATE TEMPORARY TABLE "texture_{texture_id}_end_column" (
            Start INTEGER, 
            End INTEGER, 
            Duration INTEGER,
            Velocity INTEGER, 
            Note TEXT
        );
        '''

        insert_data_command = f'''
        WITH ModifiedDurations AS (
            SELECT 
                Start,
                Velocity,
                Note,
                Duration as ModifiedDuration
            FROM "texture_{texture_id}_max_duration"
        ),
        DistinctEnds AS (
            SELECT
                Start,
                COALESCE(LEAD(Start, 1) OVER(ORDER BY Start), Start + ModifiedDuration) AS End
            FROM (SELECT DISTINCT Start, ModifiedDuration FROM ModifiedDurations) as distinct_starts
        )
        INSERT INTO "texture_{texture_id}_end_column"
        SELECT 
            m.Start,
            d.End,
            m.ModifiedDuration,
            m.Velocity,
            m.Note
        FROM ModifiedDurations m
        JOIN DistinctEnds d ON m.Start = d.Start;
        '''

        return create_table_command + '\n' + insert_data_command


    def generate_add_pitch_column_command(self, texture_id):
        return f'''
        CREATE TEMPORARY TABLE "texture_{texture_id}_base" AS 
        SELECT 
            Start,
            End,
            Velocity,
            CAST(Note AS INTEGER) AS Note,
            CAST((Note - CAST(Note AS INTEGER)) * 4095 AS INTEGER) AS Pitch
        FROM "texture_{texture_id}_end_column";
        '''
    
    
    def generate_midi_messages_table_command(self, texture_id):
        return f'''
            -- [1] Create the initial MIDI messages table:
            CREATE TEMPORARY TABLE "texture_{texture_id}_midi_messages_temp" AS
            SELECT 
                *,
                'note_on' AS Message,
                CASE 
                    WHEN ROW_NUMBER() OVER (ORDER BY Start ASC) = 1 AND Start != 0 THEN ROUND(Start * {self.ticks_per_beat})
                    ELSE 0 
                END AS Time
            FROM "texture_{texture_id}_base";

            -- [2] Update the Time column in the main table based on delta condition:
            UPDATE "texture_{texture_id}_midi_messages_temp"
            SET Time = (
                SELECT COALESCE("texture_{texture_id}_midi_messages_temp".Start - t.PreviousEnd, 0)
                FROM (
                    SELECT 
                        Start,
                        LAG(End) OVER (ORDER BY Start ASC) AS PreviousEnd
                    FROM "texture_{texture_id}_midi_messages_temp"
                ) AS t
                WHERE 
                    "texture_{texture_id}_midi_messages_temp".Start = t.Start
            )
            WHERE EXISTS (
                SELECT 1
                FROM (
                    SELECT 
                        Start,
                        LAG(End) OVER (ORDER BY Start ASC) AS PreviousEnd,
                        LAG(Start) OVER (ORDER BY Start ASC) AS PreviousStart
                    FROM "texture_{texture_id}_midi_messages_temp"
                ) AS t_sub
                WHERE 
                    "texture_{texture_id}_midi_messages_temp".Start = t_sub.Start 
                    AND "texture_{texture_id}_midi_messages_temp".Start != t_sub.PreviousEnd
                    AND "texture_{texture_id}_midi_messages_temp".Start != t_sub.PreviousStart
            );

            -- [3] Append rows for 'pitchwheel' and 'note_off' events:
            INSERT INTO "texture_{texture_id}_midi_messages_temp" (Start, End, Velocity, Note, Pitch, Message, Time)
            SELECT 
                Start, End, Velocity, Note, Pitch,
                'pitchwheel' AS Message,
                0 AS Time
            FROM "texture_{texture_id}_midi_messages_temp"
            WHERE Message = 'note_on' AND Pitch != 0.0;

            INSERT INTO "texture_{texture_id}_midi_messages_temp" (Start, End, Velocity, Note, Pitch, Message, Time)
            SELECT 
                Start, End, Velocity, Note, Pitch,
                'note_off' AS Message,
                (End - Start) * {self.ticks_per_beat} AS Time
            FROM "texture_{texture_id}_midi_messages_temp"
            WHERE Message = 'note_on';

            -- [4] Insert rows into the existing "messages" table:
            INSERT INTO "messages" (Start, End, Velocity, Note, Pitch, Message, Time)
            SELECT * FROM "texture_{texture_id}_midi_messages_temp"
            ORDER BY Start ASC;

        '''