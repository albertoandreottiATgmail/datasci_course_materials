flujos <- read.csv(file="seaflow_21min.csv",head=TRUE,sep=",")
library(caret)
inA <- createDataPartition(flujos$pop, times = 2, p = 0.5)
a <- flujos[unlist(inA[1]),1:12]
b <- flujos[unlist(inA[2]),1:12]

ggplot(data.frame(x=c(-0.25, 0.25)), aes(x=x)) + stat_function(fun=log1plusx, color="red")

qplot(flujos$pe, flujos$chl_smallcolour=flujos$pop)

#Step 4
library(rpart)
pop ~  fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small
fol <- formula(pop ~  fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fol, method="class", data=a)
print(model)
#Step 5
predict(model, b, type="vector")
prediction <- predict(model, b, type="class")==b$pop
sum(prediction == TRUE)/length(prediction)
#Step 6
library(randomForest)
model <- randomForest(fol, data=a)
prediction <- predict(model, b)
prediction <- prediction == b$pop
sum(prediction == TRUE)/length(prediction)
importance(model)
#Step 7
library(e1071)
model <- svm(fol, data=a)
prediction <- predict(model, b)
prediction <- prediction == b$pop
sum(prediction == TRUE)/length(prediction)
#Step 8, svm
model <- svm(fol, data=a)
predictions <- predict(model, b)
table(pred = predictions, true = b$pop)
#tree
model <- rpart(fol, method="class", data=a)
predictions <- predict(model, b, type="class")
table(pred = predictions, true = b$pop)
#forest
model <- randomForest(fol, data=a)
predictions <- predict(model, b)
table(pred = predictions, true = b$pop)
#Step 9
qplot(flujos$fsc_small, flujos$fsc_big)

#load all flows
flujos <- read.csv(file="seaflow_21min.csv",head=TRUE,sep=",")
library(caret)
#remove file_id 208
filtered <- flujos[flujos$file_id!="208",]

inA <- createDataPartition(filtered$pop, times = 2, p = 0.5)
a <- filtered[unlist(inA[1]),1:12]
b <- filtered[unlist(inA[2]),1:12]

#predict with svm
library(e1071)
model <- svm(fol, data=a)
prediction <- predict(model, b)
prediction <- prediction == b$pop
sum(prediction == TRUE)/length(prediction)

