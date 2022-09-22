require "matrix"

m = [60, 64, 67, 72, 76]

def generate_matrix(m)
    i = []
    y = []
    r.each do |n|
        i << (n - m.first)
        y << Array.new(m.length) {m.first + (m.first - n)}
    end
    y.each do |n| 
        m.replace(n.zip(i).map(&:sum))
    end
end

def note_to_freq(m)
    f = []
    m.each do |n|
        n.each do |o|
    a = 440
    f << (a / 32.to_f) * (2 ** ((o - 9) / 12.to_f))
        end
    end
    m.replace(f.each_slice(m.length).to_a) 
end

generate_matrix(r, m)
note_to_freq(m)

prime = Matrix.rows(m)
inversion = Matrix.columns(m)
retrograde = Matrix.rows(m.reverse)
retrograde_inversion = Matrix.columns(m.reverse)

p prime

# p note_to_freq(69)

# p m.index(&:even?)
#     i1  i2  i3  i4  i5
# p1 [60, 64, 67, 72, 76]
# p2 [56, 60, 63, 68, 72]
# p3 [53, 57, 60, 65, 69]
# p4 [48, 52, 55, 60, 64]
# p5 [44, 48, 51, 56, 60]