# roar
### 此份文件會分成以下部份進行介紹：

1. 網頁的呈現、登入畫面跟API的介紹使用
2. 排程程式的介紹

## 網頁的呈現跟API的使用

### 網頁呈現方面分成兩個部份：

1. 是我們的主要活動的呈現,在每一個活動都會有一個主題跟自己的編號,第一個頁面是給使用者查看音樂表演資訊 | 政府資料開放平臺上面的所發布的所有活動
2. 是每一個活動細節的呈現,每一個活動的部份都會有多個表演時間,在現實世界裡面,表演者也會因為諸多因素進行表演取消或表演時間更新等等,所以第二個頁面的呈現主要針對的是活動的細節。

先說明主要活動的呈現：

使用者一進入網站之後,就可以看到我們的主要畫面,會以table的形式去做呈現,這裡有使用datatable的部份,使用datatable的原因是因為可以很簡單的設定檢索資料、排序、分頁等等,方便使用者快速檢索到他要的資料。（如下圖所示）

![image](https://github.com/Jimmy850513/roar/blob/roar/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202024-08-13%2022-11-07.png)

使用者可以進行登入不登入,都可以訪問到我們的資源,但登入的使用者可以對資料進行更新、刪除等操作,如果使用者不登入的話，就無法進行操作更新、刪除等操作。

### 登入畫面介紹：

登入畫面如下,有準備好測試用的帳號可以進行登入試試看：

帳號：roar

密碼：roar1234

如果輸入錯誤的帳密,會提醒使用者帳密錯誤,如果輸入正確的帳密會跳轉回首頁。

輸入錯誤的帳密：

![螢幕快照 2024-08-11 22-44-02.png](https://github.com/Jimmy850513/roar/blob/roar/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202024-08-13%2022-12-33.png)

如果登入正確會反回到首頁,登出的按鈕就會顯示出來：



### 活動細節訪問介紹

不管你有無登入都可以訪問到活動細節,要放問活動細節的話，點選table上的任一個活動,下方會跳出訪問活動細節的按鈕：



有無登入得差別,只是可不可以對活動細節進行更新或是刪除,如果你今天是有登入的畫面會是下面這樣：



下方會有兩個對活動操作的按鈕可以使用。

無登入的話,不會有兩個按鈕,如下所示：



### API操作說明介紹

進入我們的活動細節畫面的時候,就是使用了API裡面的GET Method回傳我們活動細節的資料,但因為我們要有畫面呈現,所以我們使用了TemplateResponse來呈現畫面

### 下面先介紹APi,後面會介紹活動細節操作流程：

### 進入活動細節畫面 GET /operations/{active_id}/

- params：active_id
- Request：NO
- Response 200

```bash
{'645357a031bef61dcaf57d5c': 
{'title': '★音樂進站-讓捷運站成為你的舞台吧★邀你來表演！', 
'start_date': '2024-08-10', 'end_date': '2024-12-29', 
'active_description': '音樂進站-捷運音樂演出計畫.....', 
'active_promo_image': 'https://cloud.culture.tw/e_new_upload/...picture.jpg', 
'show_unit': '暫無演出單位', 'master_unit': '台北捷運公司', 
'sub_unit': '暫無協辦單位', 'support_unit': '暫無贊助單位', 
'other_unit': '暫無其他單位', 'show_data': [
{'id': 1, 'active_info_id': '645357a031bef61dcaf57d5c', 
'show_start_time': '2024-08-10 00:00:00', 
'show_end_time': '2024-08-10 00:00:00', 
'show_location': '台北捷運音樂進站', 
'show_location_addr': '臺北市中山站 4 號出口心中山舞臺、東區地下街
					第 2 廣場、大安森林公園站陽光大廳、松山站穹頂廣場、新店站廣場', 
'on_sale': '否', 'price': '', 'is_deleted': False},.....]}

```

- Response 404

```bash
{
	msg:'找不到資料'
}
```

### 針對更新分成兩個部份,更新我們的活動或是我們的表演細節,我主要使用OP來進行控制。

### 更新活動 PATCH /operation/{active_id}/

- Params：active_id
- Request：

```bash
{
	"title":title,
	"start_date":start_date,
	"active_description":active_description,
	"end_date":end_date,
	"show_unit":show_unit,
	"master_unit":master_unit,
	"sub_unit":sub_unit,
	"support_unit":support_unit
	"other_unit":other_unit,
	"fmTextOP2":"update_active"
}
```

- Response 200

```bash
{
	msg:'活動資訊更新成功',
	status:"OK"
}
```

- Response 404

```bash
{
	msg:'未找到匹配的對象',
	status:"ERROR"
}
```

- Response 500

```bash
{
	msg:'活動更新異常',
	status:"ERROR"
}
```

### 更新表演 PATCH /operation/{active_id}/

- Params：active_id
- Request：

```bash
{
	"show_id":show_id,
	"show_start_time":show_start_time,
	"show_end_time":show_end_time,
	"show_location":show_location,
	"show_location_addr":show_location_addr,
	"on_sale":on_sale,
	"price":price,
	"fmTextOP2":"update_show"
}
```

- Response 200

```bash
{
	msg:'表演資訊更新成功',
	status:"OK"
}
```

- Response 404

```bash
{
	msg:'找不到匹配的資料',
	status:"ERROR"
}
```

- Response 500

```bash
{
	msg:'表演資訊更新失敗'
	status:"ERROR"
}
```

### 刪除表演 PATCH /operation/{active_id}/

- Params：active_id
- Request：NO
- Response 200

```bash
{
	msg:'活動資料、表演資料刪除成功',
	status:"OK"
}
```

- Response 404

```bash
{
	msg:'匹配不到資料',
	status:"ERROR"
}
```

- Response 500

```bash
{
	msg:'刪除失敗,請重新操作',
	status:"ERROR"
}
```

以上是API的文件,下面會介紹操作方法。

更新操作方法：

當你進入活動細節畫面的時候,因為怕使用者誤key所以我們先不開放可以key資料,只能先瀏覽資料。

當你點擊下方的更新活動資訊的時候,就可以對輸入匡進行編輯,且會跳出一個確認更新的按鈕。

![螢幕快照 2024-08-12 00-31-36.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/6486e6b9-4be7-4f17-b46e-a8b6d448259c/36ac4e72-29b0-4482-9835-c7df04a0627c/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7_2024-08-12_00-31-36.png)

當你更動資料後,點選確定儲存更新,當你更新成功的時候返回提示訊息。

![螢幕快照 2024-08-12 00-32-45.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/6486e6b9-4be7-4f17-b46e-a8b6d448259c/8aef4f31-6174-46fe-8dd1-8caf25b63dab/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7_2024-08-12_00-32-45.png)

如果欲刪除活動的話,可點選刪除活動細節,就會刪除該活動,會跳轉回首頁的位置。(一樣會跳出提示窗告訴使用者刪除成功)

![螢幕快照 2024-08-12 00-34-21.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/6486e6b9-4be7-4f17-b46e-a8b6d448259c/5faf3f11-8f63-4554-9a3f-4ab5df10e52c/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7_2024-08-12_00-34-21.png)

完成後跳轉到首頁,將看不到該比資料。

如要更改表演資訊的話,可以點選table,上方就會有變更表演資訊的按鈕跳出,點選之後就可以編輯表演的資訊：

![螢幕快照 2024-08-12 00-36-04.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/6486e6b9-4be7-4f17-b46e-a8b6d448259c/7e296f94-7965-4455-a58f-8eef581808dc/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7_2024-08-12_00-36-04.png)

編輯完成後會出現在下方的table可以顯示：

![螢幕快照 2024-08-12 00-36-56.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/6486e6b9-4be7-4f17-b46e-a8b6d448259c/bd8a356a-5ef9-451f-aac5-35d5c63a3de3/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7_2024-08-12_00-36-56.png)

## 排程程式的介紹

排程程式我放在roar_api/job的資料夾,當我的apache2 server沒有停止的時候,它會依據我所設定的時間進行資料抓取。

排程程式會以每天的下午五點開始更新資料,它會固定時間抓取我們的資料到我們的Mongodb，在經由Mongodb寫入到我們的SQLite的資料庫裡面。

使用的排程的套件為apscheduler,他是使用cron的調度器進行執行,為了不要有重複的資料,且不要父改使用者已經修改過得資料,我們判斷UID為是否寫入的標準,如果UID已經存在的話,我們就不寫入進去。

排程程式我們使用的是SQL語法跟mongodb的語法來寫,我們分別使用的驅動為SQLite3跟pymongo的方式來進行資料編寫。

AWS雲端：

我在AWS虛擬機上使用apache2進行部屬,我的資料庫是使用MySQL來進行連接。

AWS的網址為公用IP:

http://35.173.191.0/,可以實際去上面操作看看。
