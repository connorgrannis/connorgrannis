library(pacman)

write_package_citations <- function() {
  # Export Citations as Bibtex (.bib)
  knitr::write_bib(file="Bibliography of packages.bib")
  
  # Table (.csv) with all information on the packages
  appendix_packages <- data.frame(Packagename = character(),
                                  Version = character(),
                                  Maintainer = character())
  
  for (pkg in p_loaded()){
    appendix_packages <- appendix_packages %>% add_row(
      Packagename = pkg,
      Version = as.character(packageVersion(pkg)),
      Maintainer = maintainer(pkg)
    )
  }
  
  write.csv(x = appendix_packages, file = "List_of_packages.csv", row.names = F)
}

write_package_citations()
