library(ggplot2)
library(reshape)

load.fem.preg <- function () {
  fem.preg <- read.table("data/2002FemPreg.csv", header = TRUE, sep=",", na.strings="None")
  fem.preg$totalwgt_oz <- fem.preg$birthwgt_lb * 16 + fem.preg$birthwgt_oz
  fem.preg$agepreg <- fem.preg$agepreg / 100
  return(fem.preg)
}

fem.preg <- load.fem.preg()

# Only interested in live births
live.births <- subset(fem.preg, outcome == 1 & prglength > 20, 
                      select = c(caseid, prglength, birthord))
live.births <- within(live.births, {
  first.born <- NA
  first.born[birthord != 1] <- "others"
  first.born[birthord == 1] <- "firsts"
})
live.births <- within(live.births, {
  timely <- NA
  timely[prglength <= 37] <- "Early"
  timely[prglength > 37 & prglength <= 40] <- "On time"
  timely[prglength > 40] <- "Late"
})

normalize <- function(xs) {
  return (xs / sum(xs))
}

count.by.week <- function(live.births) {
  melted <- melt(live.births, id.vars=c("prglength", "first.born"))
  birth.counts <- cast(melted, prglength ~ first.born, length)
  birth.counts <- within(birth.counts, {
    both <- firsts + others
  })
  return (birth.counts)
}

remaining <- function(xs) {
  return (sum(xs) - cumsum(xs) + xs)
}

plot.conditional.probs <- function(live.births) {
  probs <- within(count.by.week(live.births), {
    firsts <- firsts / remaining(firsts)
    others <- others / remaining(others)
    both <- both / remaining(both)    
  })
  melted <- melt(as.data.frame(probs), 
                 idvars=c("prglength"), 
                 measure.vars=c("firsts", "others", "both"))
  return(qplot(data=m, x=prglength, weight=value, binwidth=1) + facet_grid(variable ~ .))
}

probability.per.week <- function(live.births) {
  # Count how many births per week
  birth.counts <- count.by.week(live.births)

  # Normalize
  birth.counts <- within(birth.counts, {
    prob.firsts <- normalize(firsts)
    prob.others <- normalize(others)
    prob.both <- normalize(both)
  })

  # Compare probabilities
  birth.counts <- within(birth.counts, {diff <- prob.firsts - prob.others})
  return(birth.counts)
}

relative.risks <- function(live.births) {
  first.probs <- prop.table(table(subset(live.births, first.born == "firsts")$timely))
  other.probs <- prop.table(table(subset(live.births, first.born != "firsts")$timely))
  return(first.probs / other.probs)
}

# Graph the difference between first-born probability and others probability per 
# week of pregnancy.
birth.counts <- probability.per.week(live.births)
birth.counts$prglength <- factor(birth.counts$prglength)
qplot(data=birth.counts, x=prglength, weight=diff, binwidth=1, position="dodge")

risks <- relative.risks(live.births)

# TODO
# - Write a function that computes the probability that a baby 
#   will be born during Week N, given that it was not born prior 
#   to Week N.
# - Plot this value as a function of x for first babies and others.
