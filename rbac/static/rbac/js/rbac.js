 $(function () {
        $(".btn-del").click(function(e){
            var url = $(this).attr("data-item");
            e.preventDefault();
            Swal.fire({
              title: '真的要删除吗?',
              text: "删除将无法恢复!",
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: '确定删除',
              cancelButtonText: '取消'
            }).then(function(result) {
                if (result.value) {
                   window.location.href =url
                }
            })
        })
    });
