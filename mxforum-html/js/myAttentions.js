axios.defaults.baseURL = 'http://39.104.13.197:8000/';


let vm = new Vue({
   el:"#content",
   data:{
        join:[],
       owner:[],
       userId:store.state.userId,
       questionList:[],
       answersList:[],
       showGroup:true,
       showQuestions:false
   },
    computed:{
        user(){
            return store.state.username
        },
        notLogin(){
            return store.state.notLogin
        },

    },

    created(){
       this.showname();
        this.getMyGroup();

    },

    methods:{
        showname(){
            return store.commit('showname')
        },
        getMyGroup(){
            let that = this;
            axios.get("users/"+that.userId+"/groups/",{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((req)=>{
                that.join = req.data.msg.join;
                that.owner = req.data.msg.owner
            }).catch((err)=>{
                console.log(err)
            })
        },
        getQuestions(){
            let that = this;
            axios.get("users/"+that.userId+"/questions/",{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((req)=>{
                that.questionList = req.data
            }).catch((err)=>{
                console.log(err)
            })
        },
        getAply(){
            let that = this;
            axios.get("users/"+that.userId+"/answers/",{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((req)=>{
                that.answersList = req.data
            }).catch((err)=>{
                console.log(err)
            })
        },
        showGroup(){
            this.showQuestions = false;
            this.showGroup = true
        },
        showQuestion(){
            this.showGroup = false;
            this.showQuestions = true;
            this.getQuestions();
            this.getAply()
        }
    }

});