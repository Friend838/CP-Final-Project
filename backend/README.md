# 說明文件

## 事前準備 (有設定或安裝過就跳過)

### 1. AWS credentials

https://docs.aws.amazon.com/zh_tw/cli/latest/userguide/cli-configure-files.html

* 請先裝好AWS CLI，並輸入:
  ```
  aws configure --profile CP_team16
  ```
  access_key跟secret_access_key請在群組詢問，不要直接寫在code裡或是readme裡。

  region設定為 "us-east-1"

  format設定為 "json"

* 檢查是否有輸入成功，輸入:
  ```
  aws configure list-profiles
  ```
  並檢查是否出現CP_team16這個profile

### 2. SAM CLI 安裝

https://docs.aws.amazon.com/zh_tw/serverless-application-model/latest/developerguide/install-sam-cli.html

* 檢查是否安裝
  ```
  sam --version
  ```

### 3. 確認是不是Python3.9

* 由於lambda使用Python3.9，當SAM在編譯的時候是吃本地環境的python版本，如果不是這版本，有兩種方式:

  (1) 更換本地python版本到3.9。

  或

  (2) 安裝docker，並更改deploy.sh的第一行成
  ```
  sam build --use-container
  ```

## 部屬使用方式
* 只要有更改過code或是template.yaml，就須重新編譯。編譯成功後，就部屬至AWS。

* 如果你的電腦能夠執行腳本，直接輸入
  ```
  sh deploy.sh
  ```

* 如果不行，請執行以下兩行。
  ```
  sam build
  sam deploy
  ```
  假如你的環境不是python3.9，執行:
  ```
  sam build --use-container
  sam deploy
  ```

## 本地測試使用方式
TODO

## 程式碼檔案結構
* 分為TodosRelated和RecordsRelated。

  1. TodoRelated是所有跟代辦事項有關的API，包含creat(insert) read(query) update delete。

  2. RecordsRelated是所有跟專注紀錄有關的API，包含creat(insert) read(query) update delete。

**詳細API格式詳看hackmd。**


## 利用YANL設定所需資源
本專案用SAM部屬至AWS，以下說明template.yaml的內容
### 1. Globals: 
```
Globals:
  Function:
    Handler: app.lambda_handler
    Runtime: python3.9
    Timeout: 60
```
Global設定底下所有資源會用到的變數，如此例:

我們規範底下resource type為Function的resource，要有以下屬性:

* Handler: lambda要在app這個程式中執行lambda_handler這個function
* Runtime: 執行環境為python3.9
* Timeout: lambda最長執行時間60秒

### 2. Resource:
```
Resources:
  QueryTodosFunction:
    Type: AWS::Serverless::Function 
    Properties:
      CodeUri: TodosRelated/QueryTodos/
      FunctionName: team16_finalProject_QueryTodos
      Role: arn:aws:iam::591886860315:role/amplify-cp111065508-dev-191719-authRole-idp
      Architectures:
        - x86_64
      Events:
        queryTodos:
          Type: Api
          Properties:
            Path: /queryTodos
            Method: get
```
Resources可以定義多個resource。

在這個例子中，我們定義了一個資源，叫做「QueryTodosFunction」，資源種類為lambda function，以下是他的屬性說明:
* CodeUri: 程式碼在此專案的哪個路徑底下
* FunctionName: lambda名字叫甚麼
* Role: 執行lambda的IAM role
* Architectures: 運行lambda機器的架構
* Events: 觸發lambda的事件，由於此專案剛好需要API，因此用API觸發，我們也命名此event叫做「queryTodos」，以下為API event的屬性
  * Path: API的路徑，前贅由API gateway設定
  * Method: API觸發的方式



## 如何快速測試及Debug
要進行快速測試及Debug，通常有兩種方式，取決於所要測試的function．
由於後續的方法皆需要使用到docker，因此建議先行安裝docker．

### 一般function
在template.yaml中定義好resources後，就可以透過以下指令進行測試該function，並可以得到該function的return
```
sam local invoke "Function Name"
```
### API function
透過以下指令可以在本地透過docker建立環境以測試API 
```
sam local start-api
```
若成功運行，則會有如下訊息：
```
* Running on http://127.0.0.1:3000
2023-05-09 23:27:55 Press CTRL+C to quit
Invoking app.lambda_handler (python3.9)
```
之後便可透過postman打API進行測試
範例：http://127.0.0.1:3000/todos/query

## 問題排解

### docker 安裝問題 （MAC）
若已成功安裝docker Desktop 並確定是有運行狀態，但在使用上述測試指令時， 一直會出現以下錯誤：
```
Error: Running AWS SAM projects locally requires Docker. Have you got it installed and running?
```
請另開啟Termainal，並輸入以下指令，便能成功解決：
```
sudo ln -sf "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```
提醒：每次重新開機皆需要重新輸入

Reference: https://github.com/aws/aws-sam-cli/issues/4329


***
更多的sam template用於不同資源以及更多屬性的官飯，可查閱AWS官方文件

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-resources-and-properties.html