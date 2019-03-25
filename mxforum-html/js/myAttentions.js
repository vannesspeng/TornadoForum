axios.defaults.baseURL = 'http://127.0.0.1:8888/';


let vm = new Vue({
   el:"#content",
   data:{
       join:[],
       owner:[],
       userId:store.state.userId,
       questionList:[],
       answersList:[],
       user_nickname: "",
       user_head_url: "",
       number:true,
       showGroups:true,
       showQuestions:false,
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
       this.showGroup();
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
                that.join = req.data[2].join;
                that.owner = req.data[1].owner;
                that.user_nickname = req.data[0].user["nick_name"];
                that.user_head_url = 'http://127.0.0.1:8888' + req.data[0].user["head_url"]
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
            this.showGroups = true;
            this.showQuestions = false;            
            this.number = true;
            this.getMyGroup();
        },
        showQuestion(){
            this.showGroups = false;
            this.showQuestions = true;
            this.getQuestions();
            this.getAply();
            this.number = false
        }
    }

});