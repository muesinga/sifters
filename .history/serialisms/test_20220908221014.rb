require "~/dev/sonic-pi-projects/serialisms/modules.rb"

fund = 2
range = 50
arr = []

generate_fibonacci_sequence(fund, range, arr)
select_primes(arr)
# generate_serial_matrix(arr)

p arr