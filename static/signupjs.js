// 유효성 결과값 저장
let c_id = 0
let c_name = 0
let c_mail = 0
let c_pw = 0

// 각 input value 수정 시에 유효성 결과값 초기화.
function change_id() {
    c_id = 0
}

function change_username() {
    c_name = 0
}

function change_mail() {
    c_mail = 0
}

// 회원가입 버튼 클릭 -> DB에 회원정보 저장
function join() {
    if (c_id === 0) {
        alert("아이디를 확인을 해주세요.")
        document.getElementById("floatingId").focus()
    } else if (c_name === 0) {
        alert("닉네임을 확인 해주세요.")
        document.getElementById("floatingUsername").focus()
    } else if (!$('input:radio[name=category]').is(':checked')) {
        alert("관심사를 선택 해주세요.")
        document.getElementById("category-1").checked
    } else if (c_mail === 0) {
        alert("이메일을 확인 해주세요.")
        document.getElementById("floatingMail").focus()
    } else if (c_pw === 0) {
        alert("비밀번호를 확인 해주세요.")
        document.getElementById("floatingPassword").focus()
        document.getElementById("floatingPassword").value = null
        document.getElementById("floatingCheckPassword").value = null
    } else {
        $.ajax({
            type: "POST",
            url: "/api/signup",
            data: {
                interest_give: $('input[name=category]:checked').val(),
                id_give: $('#floatingId').val(),
                name_give: $('#floatingUsername').val(),
                mail_give: $('#floatingMail').val(),
                pw_give: $('#floatingPassword').val()
            },
            success: function (response) {
                if (response['result'] === 'success') {
                    alert('회원가입이 완료되었습니다.')
                    // 로그인 페이지 경로 지정해주기.
                    window.location.href = '/login'
                }
            }
        })
    }
}

// ID 유효성 검사
function check_id() {
    let user_id = $("#floatingId").val()
    let pattern1 = /[0-9]/; // 숫자
    let pattern2 = /[a-zA-Z]/; // 문자

    if (user_id === '') {
        alert('아이디를 입력하세요.')
    } else if (user_id.length < 8 || user_id.length > 20
        || !pattern1.test(user_id) || !pattern2.test(user_id)) {
        alert('아이디는 8~20자리 이내의 영문과 숫자로 입력해주세요.')
        document.getElementById('floatingId').value = null;
    } else {
        $.ajax({
            type: "POST",
            url: "/api/checkid",
            data: {
                id_give: user_id
            },
            success: function (response) {
                if (response['status']) {
                    c_id = 1
                    alert('사용 가능한 아이디 입니다.');
                } else {
                    alert('이미 존재하는 아이디 입니다.')
                    document.getElementById('floatingId').value = null;
                    document.getElementById("floatingId").focus()
                }
            }
        })
    }
}

// 닉네임 유효성 검사
function check_username() {
    let user_name = $("#floatingUsername").val()

    if (user_name === '') {
        alert('닉네임을 입력하세요.')
    } else if (user_name.length < 3 || user_name.length > 10) {
        alert('닉네임은 3~10자리 이내로 입력해주세요.')
    } else {
        $.ajax({
            type: "POST",
            url: "/api/checkname",
            data: {
                name_give: user_name
            },
            success: function (response) {
                if (response['status']) {
                    c_name = 1
                    alert('사용 가능한 닉네임 입니다.')
                } else {
                    alert('이미 존재하는 닉네임 입니다.')
                    document.getElementById('floatingUsername').value = null;
                    document.getElementById("floatingUsername").focus()
                }
            }
        })
    }
}

// 이메일 유효성 검사
function check_mail() {
    let user_mail = $("#floatingMail").val()

    let pattern = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

    if ($('#floatingMail').val() === '') {
        alert('이메일을 입력하세요.')
    } else if (!pattern.test(user_mail)) {
        alert('이메일 형식으로 입력해주세요.')
        document.getElementById('floatingMail').value = null;
    } else {
        $.ajax({
            type: "POST",
            url: "/api/checkmail",
            data: {
                mail_give: user_mail
            },
            success: function (response) {
                if (response['status']) {
                    c_mail = 1
                    alert('사용 가능한 이메일 입니다.')
                } else {
                    alert('이미 존재하는 이메일 입니다.')
                    document.getElementById('floatingMail').value = null;
                    document.getElementById("floatingMail").focus()
                }
            }
        })
    }
}

// 비밀번호 유효성 검사
function check_pw1() {
    let user_pw = $('#floatingPassword').val()
    let pattern1 = /[0-9]/
    let pattern2 = /[a-zA-Z]/

    let user_id = $('#floatingId').val()

    if (user_pw.length < 10 || !pattern1.test(user_pw) || !pattern2.test(user_pw)) {
        alert('비밀번호는 10자리 이상 영문과 숫자로 입력해주세요.')
        document.getElementById("floatingPassword").value = null;
        document.getElementById("floatingPassword").focus()
    } else if (user_pw === user_id) {
        alert('비밀번호에 아이디가 포함될 수 없습니다.')
        document.getElementById("floatingPassword").value = null;
        document.getElementById("floatingPassword").focus()
    } else {
        document.getElementById("floatingCheckPassword").focus()
    }
}

// 비밀번호 확인. 비밀번호와 동일한지 검사
function check_pw2() {
    let user_pw1 = $('#floatingPassword').val()
    let user_pw2 = $('#floatingCheckPassword').val()

    if (user_pw2 === '') {
        $('.msg').text("")
    } else if (user_pw1 !== user_pw2) {
        c_pw = 0
        $('.msg').css('color', 'red');
        $('.msg').text("비밀번호가 일치하지 않습니다.")
    } else {
        c_pw = 1
        $('.msg').css('color', 'blue');
        $('.msg').text("비밀번호가 일치 합니다.")
    }
}