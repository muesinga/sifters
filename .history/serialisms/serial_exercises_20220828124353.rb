require "matrix"
require "./test.rb"

# use_synth :saw
# use_bpm 60

# m = [60, 64, 67, 72, 76]

# def generate_matrix(m)
#     x = []
#     y = []
#     z = []
#     m.each do |n|
#         x << (n - m.first)
#         y << Array.new(m.length) {m.first + (m.first - n)}
#     end
#     y.each do |n| 
#         z << n.zip(x).map(&:sum)
#     end
#     m.replace(z)
# end

# def midi_to_freq(m)
#     f = []
#     m.each do |n|
#         n.each do |o|
#             a = 440
#             f << (a / 32.to_f) * (2 ** ((o - 9) / 12.to_f))
#         end
#     end
#     m.replace(f.each_slice(m.length).to_a) 
# end

# generate_matrix(m)
# midi_to_freq(m)

# loop do
# in_thread do 
#     prime.each do |m|
#     play hz_to_midi(2*(m/3.14))
#     sleep m/314
#     end
# end

# inversion.each do |n|
#     play hz_to_midi(2*(n/3.14))
#     sleep n/314
# end
# end