
axios.defaults.baseURL = 'http://127.0.0.1:8888/';

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
        image:'../../images/middle.jpg',
        oldpsw:'',
        newpsw:'',
        confirmpsw:''
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
        getRadioVal(event){
            let that = this;
            that.userInfo.gender = event.target.value;
            console.log(that.userInfo.gender)
        }, 
        getInfo(){
            let that = this;
            axios.get("/info/",{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((res)=>{
                that.userInfo = res.data;
                if(that.userInfo.address === null){
                    that.userInfo.address = 'null'
                }
            }).catch((err)=>{
                console.log(err)
            })
        },
        changeInfo(){
            let that = this;
            axios.patch("/info/",{
                "nick_name":that.userInfo.nick_name,
                "gender":that.userInfo.gender,
                "address":that.userInfo.address,
                "desc":that.userInfo.desc
            },{
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((res)=>{
                console.log(res.data)
                alert('个人信息保存成功！')
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
                        "tsessionid": store.state.tesssionid,
                        "Content-Type": "multipart/form-data"
                    }
            }).then((res)=>{
                alert("头像修改成功！")
                that.image = 'http://127.0.0.1:8888' + res.data.image
            }).catch((err)=>{
                alert("文件上传失败，请尝试重新上传！")
                console.log(err)
            })
        },
        changePsw(){
            let that = this;
            axios.post("/password/",{
                "old_psw":that.oldpsw,
                "new_psw":that.newpsw,
                "confirm_psw":that.confirmpsw
            }, {
                headers:{
                    "tsessionid": store.state.tesssionid,
                }
            }).then((res)=>{
                alert("密码修改成功！")
            }).catch((err)=>{
                alert("密码修改失败！")
                console.log(err)
            })
        }
    }
})