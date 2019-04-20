<h1><b>爬取bilibili视频封面</b></h1>
<hr/>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;昨晚学习英语听力，偶然间“遇到”了JFla翻唱的《Something Just Like This》的视频，看完之后被小姐姐
的声音和侧颜吸引住了，于是我去了万能的b站，搜了一下果然有很多。当时正好在学爬虫，比较菜，想练练手。于是我就说蠢了一下，干脆把搜到的所有视频的av号和封面以
及标题都爬下来吧，满足于一下自己的双面需求。因此将实现的想法和过程放出来，大家可以一起讨论。(图片也上传了哟)</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;然后就开始爬，先在b站搜索JFla</p>
<div align="center"><img src="https://github.com/foreversunx/GetbilibiliPic/blob/master/1.png" width="600" height="300" /></div>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;可以看到我们搜到了很多，大概一共有50页的样子。既然是爬取封面，那就先看一下这个页面的源码，万一链接在里面呢，虽然可能性比较小，但是还是看看吧。</p>
<div align="center"><img src="https://github.com/foreversunx/GetbilibiliPic/blob/master/2.png" width="600" height="300" /></div>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;好吧，可以看到src="",alt=""是空的，说明封面图片不在这，但是我们能看到，不仅标题在这里，视频的av号也在这里，觉得有可能有用，先标注一下。然后就只能去network里面找了，找来找去没找着......算了，不找了！干脆暴力一点，随便找一个视频点进去，打开network，我就不信找不到你！</p>
<div align="center"><img src="https://github.com/foreversunx/GetbilibiliPic/blob/master/3.png" width="600" height="300" /></div>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;找到view？aid=****...**文件，打开preview一下，果然，被我找到了，可算发现你了。发现pic链接，就是它了，我们就准备获取它。复制它的adress，发现是 https://api.bilibili.com/x/web-interface/view?aid=9467312 于是我们猜测，每个视频包含我们想要数据的链接都长这样，只是aid即av号不一样而已，再随便打开几个看一下，证实了这个想法。那就好办了，之前不是说网页源码可以获取本页视频av号嘛，那就搞！</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们根据源码页面的链接构造，改变page属性就可以轻松实现翻页，有多少page也可以爬下来，按着源码往下找找就行了。然后写个循环吧，把所有页面的av号和标题拿下来，存到数据库里面去。爬完以后，就从数据读取av号，完成最终url的拼接，这样我们就得到了所有视频包含数据的url，循环爬取信息，拿到我们想要的封面链接，保存到数据库里面，然后用requests包，写个方法，把图片下载下来就完事了，慢慢的爬，悄悄地，别被发现了。</p>
<div align="center"><img src="https://github.com/foreversunx/GetbilibiliPic/blob/master/4.png" width="600" height="300" /></div>
<p>如果有不恰当的地方，希望大家指正！一起努力学习！</p>
