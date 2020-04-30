function $(selector, context) {
	return (context || document).querySelector(selector);
}

function $$(selector, context) {
	return [].slice.call((context || document).querySelectorAll(selector));
}
$$(".button-box").forEach(function (el) {
	if ($$("button", el).length === 1) {
		$("button", el).style.cssText = "margin:0 auto;";
	}
})
$(".container").style.display = "block";

$$(".button-box button").forEach(function (btn, index) {
	btn.onclick = function () {
		Dialog({
			title: "人员信息" + index,
			content: '姓名：<br>性别：<br>律所任职：<br>律师证号：<br>执业日期：<br>执业年限：<br>律师职称：<br>优势类型：<br>其他职称：<br>社会任职：'
		});

	}
})


