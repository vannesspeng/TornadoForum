/**
 * Created by Think on 2018/8/11.
 */

new Vue({
    el:"#questions",

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
        getquestions () {
            console.log(store.state.notLogin);
            let that = this;
            axios.get("http://127.0.0.1:8888/questions/",{
                params:{
                    "o":"new",
                    "c":"技术分享"
                }
            })
                .then(function(response){
                    that.res = response.data
                })
                .catch(function(err){
                    console.log(err);
                });

        },
        showname(){
           return store.commit('showname')
        }

}
})




