/**
 * Created by Think on 2018/8/8.
 */

var ue = UE.getEditor('container');
var html;
ue.ready(function () {
    html = ue.getContent();
});
axios.defaults.baseURL = 'http://127.0.0.1:8888/';
function getQueryString(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null) return unescape(r[2]); return null; 
} 

let vm = new Vue({
    el:"#content",
    data:{
        title:'',
        thisGroup:{},
        groupId:'',
        notLogin:false
    },
    created(){
        this.getGroup();
    },
    methods:{
        getGroup(){
            let that = this;
            this.getGroupId();
            if(!store.state.tesssionid){
                location.href = '../../login.html';
                that.notLogin = false
            }else {
                that.notLogin = true
            }
            axios.get('/groups/'+that.groupId+'/',{
                headers:{
                    "tsessionid":store.state.tesssionid
                }
            }).then((req)=>{
               that.thisGroup = req.data;
               //处理小组的数组，将需要的groupID对应的小组赋值给thisGroup
            }).catch((err)=>{
                console.log(err)
            })
        },
        getGroupId(){
            this.groupId = getQueryString("groupId");
            if(!store.state.tesssionid){
                location.href = '../../login.html';
                this.notLogin = false
            }else {
                this.notLogin = true
            }
            console.log(this.notLogin)
        },
        addPost(){
            let that = this;
            var ue = UE.getEditor('container');
            var html;
            ue.ready(function () {
                html = ue.getContent();
            });
            axios.post("/groups/"+that.groupId+"/posts/",{
                "title":that.title,
                "content":html
            },{
                headers:{
                    "tsessionid":store.state.tesssionid
                }
            }).then(()=>{
                location.href = './postsList.html?groupid='+that.groupId
            }).catch((err)=>{
                console.log(err)
            })
        }
    },
    computed:{
        user:function () {
            return store.state.username
        }
    }
});












