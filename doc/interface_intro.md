# 随手记 文本处理平台 接口说明


## 1. 搜索引擎

Args:

| Args          | Description    | Default   |
| ------------- | :------------- | :-----    |
| size          | Query Size     | 10        |
| page          | page count     | 1         |
| query         | query content  | NECESSARY |


Result :

	{
	"timetook": 4044,
	"mount": 46838,
	"query": "理财",
	"resList": [
	{
		"content": "{:5_100:}",
		"authorid": 1672307,
		"author": "2635260947",
		"lastpost": 1415193596,
		"replies": 12,
		"url": "http://bbs.feidee.com/thread-353845-1-1.html",
		"dateline": 1409195406,
		"views": 1877,
		"id": "353845",
		"subject": "理财 理财"
	
	},
	{
		"content": "天天理财，天天快乐，天天理财，天天生活就规律",
		"authorid": 2421341,
		"author": "2643153219",
		"lastpost": 1419572956,
		"replies": 20,
		"url": "http://bbs.feidee.com/thread-397496-1-1.html",
		"dateline": 1418312104,
		"views": 193,
		"id": "397496",
		"subject": "理财理财了"
	}
	],
	"page": 1,
	"size": 2
	
	}

Result Table :

| Parameters    | Description       |
| ------------- | :-------------    |
| size          | query Size        |
| page          | page count        |
| query         | query content     |
| timetook      | time query took   |
| resList       | elements returned |





### 1.1 社区帖子搜索

URL :  http://192.168.241.113:23333/json/thread/query?size=10&page=1

### 1.2 社区用户搜索

URL :  http://192.168.241.113:23333/json/user/query?size=10&page=1


### 1.3 论坛版块搜索

URL :  http://192.168.241.113:23333/json/forums/query?size=10&page=1




## 2.文本分词引擎

从文章中提取关键词。

URL :  http://192.168.241.113:23333/json/wordsplit/content?=content

Args

| Args          | Description    | Default   |
| ------------- | :------------- | :-----    |
| content       | split content  | NECESSARY |


## 3.推荐引擎

## 3.1社区推荐引擎

### 3.1.1 推荐引擎取推荐结果

URL :  http://192.168.241.113:23333/recommendation/forum/get?uid=121&topk=3


Args:

| Args          | Description          | Default                   |
| ------------- | :-------------       | :--------------           |
| uid           | the uid recommend to | NECESSARY(OR UUID SETTED) |
| uuid          | the uid recommend to | NECESSARY(OR UID SETTED)  |
| topk          | the query amount     | 3                         |


Returns :


| Parameters             | Description                         |
| -------------          | :-------------                      |
| status                 | uid found?                          |
| recommendation_content | the query amount                    |
| score                  | result score, sorted by this param  |
| reason                 | recommendation reason               |
| recommend_tid          | recommend tid (relate to forum tid) |
| date                   | timestamp of forum recommended      |


	{
	    "status": true,
	    "recommendation_content": [
	        {
	            "date": 1431620182,
	            "recommend_tid": "467106",
	            "reason": {
	                "like": 364863
	            },
	            "score": 0.03193364674165094
	        },
	        {
	            "date": 1426831651,
	            "recommend_tid": "441873",
	            "reason": {
	                "like": 364863
	            },
	            "score": 0.02475006064943133
	        },
	        {
	            "date": 1426438499,
	            "recommend_tid": "440067",
	            "reason": {
	                "like": 365490
	            },
	            "score": 0.024438104744718032
	        }
	    ],
	    "took": 7
	}




### 3.1.2 推荐引擎取全量推荐结果

URL :  http://192.168.241.113:23333/recommendation/forum/getall?uid=121

Args:

| Parameters    | Description          | Default                   |
| ------------- | :-------------       | :--------------           |
| uid           | the uid recommend to | NECESSARY(OR UUID SETTED) |
| uuid          | the uid recommend to | NECESSARY(OR UID SETTED)  |
