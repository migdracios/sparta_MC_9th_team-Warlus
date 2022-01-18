// 마우스 스크롤 펑션 스크립트
function scroll(){
        var offset = $("#map").offset(); //선택한 태그의 위치를 반환

            //animate()메서드를 이용해서 선택한 태그의 스크롤 위치를 지정해서 0.4초 동안 부드럽게 해당 위치로 이동함

            $("html").animate({scrollTop: offset.top}, 400);
    }

//스크롤에대한 jquery 입니다.
      $(document).ready(function () {
        $("#btn1,#btn2,#btn3,#btn4").click(function () {
            var offset = $("#map").offset(); //선택한 태그의 위치를 반환

            //animate()메서드를 이용해서 선택한 태그의 스크롤 위치를 지정해서 0.4초 동안 부드럽게 해당 위치로 이동함

            $("html").animate({scrollTop: offset.top}, 400);
        });
    });