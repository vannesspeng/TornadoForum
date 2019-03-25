/**
 * Created by Think on 2018/8/11.
 */

new Vue({
    el:"#questions",
    data:{
        category:'all',
        number:1
    },

    created(){
        this.showname();
        this.getquestions()
    },

    data(){
        return{
            res:[]
        }
    },
    computed:{
        user(){
            return store.state.username
        },
        notLogin(){
            return store.state.notLogin
        }
    },

    methods:{
        getquestions (category) {
            console.log(store.state.notLogin);
            let that = this;
            axios.get("http://127.0.0.1:8888/questions/",{
                params:{
                    "o":"new",
                    "c":category
                }
            })
                .then(function(response){
                    that.res = response.data
                    if(store.state.tesssionid){
                        that.notLogin = true
                    }else {
                        that.notLogin = false
                    }
                })
                .catch(function(err){
                    console.log(err);
                });
            if(category == ''){
                that.number = 1
            }else if(category == '技术问答'){
                that.number = 2
            }else if(category == '技术分享'){
                that.number = 3
            }

        },
        showname(){
           return store.commit('showname')
        }

}
})




