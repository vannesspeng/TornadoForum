
axios.defaults.baseURL = 'http://39.104.13.197:8000/';

let vm = new Vue({
    el:'#content',
    data:{
        userInfo:{},
        nick_name:"",
        desc:"",
        gender:"",
        address:"",
        showInfo:true,
        showPsd:false,
        showImg:false,
        front_img:'',
        file:'',
        image:'../../images/middle.jpg'
    },
    computed:{
        user(){
            return store.state.username
        },
        notLogin(){
            return store.state.notLogin
        }
    },
    created(){
        this.showname();
        this.getInfo()
    },
    methods:{

        showname(){
            return store.commit('showname')
        },
        getInfo(){
            let that = this;
            axios.get("/profiles/",{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((res)=>{
                that.userInfo = res.data;
                if(that.userInfo.address === null){
                    that.userInfo.address = 'null'
                }
                if(that.userInfo.gender =='male'){
                    that.userInfo.gender = '2'
                }else {
                    that.userInfo.gender = '1'
                }
            }).catch((err)=>{
                console.log(err)
            })
        },
        changeInfo(){
            let that = this;
            if(that.userInfo.gender ==2){
                that.userInfo.gender = 'female'
            }else {
                that.userInfo.gender = 'male'
            }
            axios.patch("/profiles/",{
                "nick_name":that.userInfo.nick_name,
                "gender":that.userInfo.gender,
                "address":that.userInfo.address,
                "desc":that.userInfo.desc
            },{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((res)=>{

            }).catch((err)=>{
                console.log(err)
            })
        },
        showimg(){
            this.showInfo = false;
            this.showImg = true;
            this.showPsd = false
        },
        showinfo(){
            this.showInfo = true;
            this.showImg = false;
            this.showPsd = false
        },
        showpsd(){
            this.showInfo = false;
            this.showImg = false;
            this.showPsd = true
        },

        //头像
        changeImage: function(e){
            this.file = e.target.files[0];
        },
        postImg(){
            let that = this;
            let formData = new FormData();
            formData.append('image', this.file);
            axios.post("/headimages/",formData
            ,{
                    headers:{
                        "tsessionid": store.state.tesessionid,
                        "Content-Type": "multipart/form-data"
                    }
            }).then((res)=>{
                that.image = 'http://39.104.13.197:8000' + res.data.image
            }).catch((err)=>{
                console.log(err)
            })
        }
    }
})