arr = [0, 1, 1, 2, 3, 5, 8, 13]
def generate_fibonacci_matrox
arr.each do |y|
sub_arr = []
    if y == 0
        i = 1
        arr.length.times do
            sub_arr << y 
            y, i = i, y + i
        end
    else
        i = 0
        arr.length.times do 
            sub_arr << y
            i, y = y, i + y
        end 
    end
p sub_arr
end