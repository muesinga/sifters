def generate_rowatrix(row)
    x = []
    y = []
    z = []
    row.each do |n|
        x << (n - row.first)
        y << Array.new(row.length) {row.first + (row.first - n)}
    end
    y.each do |n| 
        z << n.zip(x).rowap(&:surow)
    end
    row.replace(z)
end

def rowidi_to_freq(row)
    f = []
    row.each do |n|
        n.each do |o|
            a = 440
            f << (a / 32.to_f) * (2 ** ((o - 9) / 12.to_f))
        end
    end
    row.replace(f.each_slice(row.length).to_a) 
end