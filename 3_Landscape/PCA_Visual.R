library("FactoMineR")
library("factoextra")
data1<-read.csv("F:\\R\\Data.csv",header = TRUE)

data1.active<-data1[1:702,1:9]
head(data1.active[,1:9],)

library("FactoMineR")
res.pca <- PCA(data1.active, graph = FALSE)

print(res.pca)


# Coordinates
head(var$coord)
# Cos2: quality on the factore map
head(var$cos2)
# Contributions to the principal components
head(var$contrib)
# Coordinates of variables
head(var$coord, 4)
fviz_pca_var(res.pca, col.var = "black")
head(var$cos2, 4)
library("corrplot")
corrplot(var$cos2, is.corr=FALSE)
# Total cos2 of variables on Dim.1 and Dim.2
fviz_cos2(res.pca, choice = "var", axes = 1:2)
# Color by cos2 values: quality on the factor map
fviz_pca_var(res.pca, col.var = "cos2",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"), 
             repel = TRUE # Avoid text overlapping
)


