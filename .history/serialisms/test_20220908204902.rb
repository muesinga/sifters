require 'prime'
require 'matrix'

Prime.each(100) do |prime|
    p prime  #=> 2, 3, 5, 7, 11, ...., 97
  end

a = Matrix[[0]]

p a