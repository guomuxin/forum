<template>
  <div class="sign">
    <div class="logo"><a href="/"><img src="/static/image/nav-logo.png" alt="Logo"></a></div>
    <div class="main">
      <h4 class="title">
        <div class="normal-title">
          <router-link to="/login">登录</router-link>
          <b>·</b>
          <router-link id="js-sign-up-btn" class="active" to="/register">注册</router-link>
        </div>
      </h4>

      <div class="js-sign-up-container">
        <form class="new_user" id="new_user" action="" accept-charset="UTF-8" method="post">
          <div class="input-prepend restyle">
            <input placeholder="你的昵称" type="text" value="" v-model="nickname" id="user_nickname">
            <i class="iconfont ic-user"></i>
          </div>
          <div class="input-prepend restyle no-radius js-normal">
            <input placeholder="手机号" type="tel" v-model="mobile" id="user_mobile_number">
            <i class="iconfont ic-phonenumber"></i>
          </div>
          <div class="input-prepend restyle no-radius security-up-code js-security-number" v-if="is_show_sms_code">
            <input type="text" v-model="sms_code" id="sms_code" placeholder="手机验证码">
            <i class="iconfont ic-verify"></i>
            <a tabindex="-1" class="btn-up-resend js-send-code-button" :class="{disable:send_able}"
               href="javascript:void(0);" id="send_code" @click="send_sms">{{sms_code_text}}</a>
          </div>
          <input type="hidden" name="security_number" id="security_number">
          <div class="input-prepend">
            <input placeholder="设置密码" type="password" v-model="password" id="user_password">
            <i class="iconfont ic-password"></i>
          </div>
          <input type="submit" name="commit" value="注册" class="sign-up-button" id="sign_up_btn"
                 @click.prevent="registerHandler" data-disable-with="注册">
          <p class="sign-up-msg">点击 “注册” 即表示您同意并愿意遵守<br> <a target="_blank" href="">用户协议</a> 和 <a target="_blank"
                                                                                                  href="">隐私政策</a> 。</p>
        </form>
        <!-- 更多注册方式 -->
        <div class="more-sign">
          <h6>社交帐号直接注册</h6>
          <ul>
            <li><a id="weixin" class="weixin" target="_blank" href=""><i class="iconfont ic-wechat"></i></a></li>
            <li><a id="qq" class="qq" target="_blank" href=""><i class="iconfont ic-qq_connect"></i></a></li>
          </ul>

        </div>
      </div>

    </div>
  </div>
</template>

<script>
  export default {
    name: "Register",
    data() {
      return {
        nickname: "",
        mobile: "",
        sms_code: "",
        password: "",
        sms_code_text: "发送验证码",
        is_show_sms_code: false,
        send_able: false
      }
    },
    watch: {
      mobile() {
        if (/^1[3-9]\d{9}$/.test(this.mobile)) {
          this.is_show_sms_code = true;
          this.check_mobile_unique()
        } else {
          this.is_show_sms_code = false
          this.send_able = false

        }
      }
    },
    methods: {
      check_mobile_unique() {
        this.$axios.get(this.$settings.Host + `/users/mobile/${this.mobile}/`).then((response) => {
        }).catch((err) => {
          this.$message.error(err.response.data.err_msg)
          this.send_able = true
        })
      },
      registerHandler() {
        this.$axios.post(this.$settings.Host + `/users/register/`,
          {
            nickname: this.nickname,
            mobile: this.mobile,
            password: this.password,
            sms_code: this.sms_code,
          }).then((response) => {
          localStorage.removeItem("user_token");
          localStorage.removeItem("user_id");
          localStorage.removeItem("user_name");
          localStorage.removeItem("user_avatar");
          localStorage.removeItem("user_nickname");
          sessionStorage.user_token = response.data.token;
          sessionStorage.user_id = response.data.id;
          sessionStorage.user_name = response.data.username;
          sessionStorage.user_avatar = response.data.avatar;
          sessionStorage.user_nickname = response.data.nickname;
          this.$confirm('注册成功, 欢迎加入forum！', '提示', {
            confirmButtonText: '跳转到首页',
            cancelButtonText: '跳转上一页',
            type: 'success'
          }).then(() => {
            this.$router.push("/");
          }).catch(() => {
            this.$router.go(-1);
          });
        }).catch((error) => {
          this.$message(error.response.data)
          console.log(error.response.data)
        })
      },
      send_sms() {
        this.$axios.get(this.$settings.Host + `/users/sms/${this.mobile}/`).then((response) => {
          console.log(response.data)
        }).catch((error) => {
          if(error.response.data.non_field_errors){

            this.$message(error.response.data.non_field_errors[0])
          }
          console.log(error.response.data)
        })
        let timer = 60
        let t = setInterval(() => {
          if (--timer < 1) {
            this.sms_code_text = "发送验证码";
            this.send_able = false
            clearInterval(t);
          }
          else{
            this.sms_code_text = `${timer}秒后重新发送`
            this.send_able = true
          }
        },1000)

      }
    }
  }
</script>

<style scoped>
  input {
    outline: none;
  }

  *, :after, :before {
    box-sizing: border-box;
  }

  .sign {
    height: 100%;
    min-height: 750px;
    text-align: center;
    font-size: 14px;
    background-color: #f1f1f1
  }

  .sign:before {
    content: "";
    display: inline-block;
    height: 85%;
    vertical-align: middle
  }

  .sign .disable {
    opacity: .5;
    pointer-events: none
  }

  .sign .tooltip-error .tooltip-inner i {
    position: static;
    margin-right: 5px;
    font-size: 20px;
    color: #ea6f5a;
    vertical-align: middle
  }

  .sign .tooltip-error .tooltip-inner span {
    vertical-align: middle;
    display: inline-block;
    white-space: normal;
    max-width: 230px
  }


  .sign .slide-error i {
    position: static !important;
    margin-right: 10px;
    color: #ea6f5a !important;
    vertical-align: middle
  }

  .sign .slide-error span {
    font-size: 15px;
    vertical-align: middle
  }

  .sign .slide-error div {
    margin-top: 10px;
    font-size: 13px
  }

  .sign .slide-error a {
    color: #3194d0
  }


  .sign .logo {
    position: absolute;
    top: 56px;
    margin-left: 50px
  }

  .sign .logo img {
    width: 100px
  }

  .sign .main {
    width: 400px;
    margin: 60px auto 0;
    padding: 50px 50px 30px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 0 8px rgba(0, 0, 0, .1);
    vertical-align: middle;
    display: inline-block
  }

  .sign .title {
    margin: 0 auto 50px;
    padding: 10px;
    font-weight: 400;
    color: #969696
  }

  .sign .reset-title a, .sign .title a {
    padding: 10px;
    color: #969696
  }

  .sign .reset-title a:hover, .sign .title a:hover {
    border-bottom: 2px solid #ea6f5a
  }

  .sign .reset-title .active, .sign .title .active {
    font-weight: 700;
    color: #ea6f5a;
    border-bottom: 2px solid #ea6f5a
  }

  .sign .reset-title b, .sign .title b {
    padding: 10px
  }

  .sign form {
    margin-bottom: 30px
  }

  .sign form .input-prepend {
    position: relative;
    width: 100%
  }

  .sign form .input-prepend input {
    width: 100%;
    height: 50px;
    margin-bottom: 0;
    padding: 4px 12px 4px 35px;
    border: 1px solid #c8c8c8;
    border-radius: 0 0 4px 4px;
    background-color: hsla(0, 0%, 71%, .1);
    vertical-align: middle
  }

  .sign form .input-prepend i {
    position: absolute;
    top: 14px;
    left: 10px;
    font-size: 18px;
    color: #969696
  }

  .sign form .input-prepend span {
    color: #333
  }

  .sign form .restyle {
    margin-bottom: 0
  }

  .sign form .restyle input {
    border-bottom: none;
    border-radius: 4px 4px 0 0
  }

  .sign form .no-radius input {
    border-radius: 0
  }


  .sign form .slide-security-placeholder p {
    padding-top: 7px;
    color: #999;
    margin-right: -7px
  }

  .sign .remember-btn span {
    margin-left: 5px;
    font-size: 15px;
    color: #969696;
    vertical-align: middle
  }

  .sign .forget-btn a {
    color: #999
  }

  .sign .forget-btn a:hover {
    color: #333
  }


  .sign .forget-btn .dropdown-menu a {
    padding: 10px 20px;
    color: #333
  }

  .sign .sign-up-msg {
    margin: 10px 0;
    padding: 0;
    text-align: center;
    font-size: 12px;
    line-height: 20px;
    color: #969696
  }

  .sign .sign-up-msg a, .sign .sign-up-msg a:hover {
    color: #3194d0
  }

  .sign .overseas input {
    padding-left: 110px !important
  }

  .sign .overseas .overseas-number span {
    margin-top: 17px;
    padding-left: 35px;
    text-align: left;
    font-size: 14px;
    display: block
  }


  .sign .overseas .dropdown-menu li a {
    padding: 6px 20px;
    font-size: 14px;
    line-height: 20px
  }

  .sign .overseas .dropdown-menu li a::hover {
    color: #fff;
    background-color: #f5f5f5
  }

  .sign .more-sign {
    margin-top: 50px
  }

  .sign .more-sign h6 {
    position: relative;
    margin: 0 0 10px;
    font-size: 12px;
    color: #b5b5b5
  }

  .sign .more-sign h6:before {
    left: 30px
  }

  .sign .more-sign h6:after, .sign .more-sign h6:before {
    content: "";
    border-top: 1px solid #b5b5b5;
    display: block;
    position: absolute;
    width: 60px;
    top: 5px
  }

  .sign .more-sign h6:after {
    right: 30px
  }

  .sign .more-sign ul {
    margin-bottom: 10px;
    list-style: none
  }

  .sign .more-sign ul li {
    margin: 0 5px;
    display: inline-block
  }

  .sign .more-sign ul a {
    width: 50px;
    height: 50px;
    line-height: 50px;
    display: block
  }

  .sign .more-sign ul i {
    font-size: 28px
  }

  .sign .more-sign .ic-wechat {
    color: #00bb29
  }

  .sign .more-sign .ic-qq_connect {
    color: #498ad5
  }

  .sign .return i {
    margin-right: 5px
  }

  .geetest_panel_box > * {
    box-sizing: content-box
  }

  .sign .sign-in-button, .sign .sign-up-button {
    margin-top: 20px;
    width: 100%;
    padding: 9px 18px;
    font-size: 18px;
    border: none;
    border-radius: 25px;
    color: #fff;
    background: #42c02e;
    cursor: pointer;
    outline: none;
    display: block;
    clear: both
  }

  .sign .sign-in-button:hover, .sign .sign-up-button:hover {
    background: #3db922
  }

  .sign .btn-in-resend {
    background-color: #3194d0
  }

  .sign .sign-up-msg {
    margin: 10px 0;
    padding: 0;
    text-align: center;
    font-size: 12px;
    line-height: 20px;
    color: #969696
  }

  .sign .btn-in-resend, .sign .btn-up-resend {
    position: absolute;
    top: 7px;
    right: 7px;
    width: 100px;
    height: 36px;
    font-size: 13px;
    color: #fff;
    background-color: #42c02e;
    border-radius: 20px;
    line-height: 36px
  }

  .sign .btn-in-resend {
    background-color: #3194d0
  }

  .sign .sign-up-msg {
    margin: 10px 0;
    padding: 0;
    text-align: center;
    font-size: 12px;
    line-height: 20px;
    color: #969696
  }
</style>
