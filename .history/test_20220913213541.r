print comb <- function(n, k) {
    all <- combn(0:n, k)
    sums <- colSums(all)
    all[, sums == n]
}

 comb(10, 2)