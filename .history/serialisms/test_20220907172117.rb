arr = [0, 1]

range = 10
i = 0
y = 3



range.times do 
    p i
    i, y = y, i + y
end