const tesssionid = this.$cookies.get("tesssionid");
let username = this.$cookies.get("nick_name");
const userId = this.$cookies.get("user_id");
const default_url = "http://127.0.0.1:8888"
const store = new Vuex.Store({
    state:{
        tesssionid,
        username,
        notLogin:false,
        userId
    },
    mutations:{
        showname(state){
            if(!state.username){
                location.href = '../login.html';
                state.notLogin = false
            }else{
                state.notLogin = true
            }
        }

    }
})

