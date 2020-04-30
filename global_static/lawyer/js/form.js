window.onload=function(){
    var form_login = document.querySelector('.form_login')
    var form_register = document.querySelector('.form_register')
    var switchBtns = document.querySelectorAll('.switch')

    switchBtns.forEach(function(item){
        item.addEventListener('click',function(){
            if(this.innerText=='返回登录'){
                addStyle(form_login,{ height: '0',transitionDelay:'0s'})
                addStyle(form_register,{height: '422px',transitionDelay: '1.2s'})
            }else if(this.innerText=='修改密码'){
                addStyle(form_login,{ height: '422px', transitionDelay: '1.2s'})
                addStyle(form_register,{height: '0',transitionDelay:'0s'})
            }
        })
    })

    function addStyle(ele,orignStyle){
        for(var item in orignStyle){
            if(ele){
                ele.style[item] = orignStyle[item] 
            }
        }
    }
   
}