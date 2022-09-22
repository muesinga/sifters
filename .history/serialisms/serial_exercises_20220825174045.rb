require "matrix"
require "sonic-pi"

# sonic_pi use_synth :piano

r = [77, 65, 44, 82, 33]
m = []

def generate_matrix(r, m)
  i = []
  y = []
  r.each do |n|
    i << (n - r.first)
    y << Array.new(r.length) {r.first + (r.first - n)}
  end
  y.each do |n|
    m << n.zip(i).map(&:sum)
  end
end

generate_matrix(r, m)

m = Matrix.rows(m)

m.each do |n|
  sonic_pi play n
  sleep 0.5
end