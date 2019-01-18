/**
 * Created by Think on 2018/7/14.
 */
axios.defaults.baseURL = 'http://127.0.0.1:8888/';
let vm = new Vue({
    el:"#content",
    data:{
        groupMsg:[],
        hotGroup:[],
        showDialog:"none",
        groupId:'',
        apply_reason:'',
        token:'',
        category:'all',
        number:1,
        hotnumber:true
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
        this.getGroup("");
        this.hottGroup("hot")
    },
    methods:{
        getGroup(category){
            let that = this;
            that.category = category;
            axios.get('/groups/?c='+category + "&o=new",{
                }).then(function (req) {
                that.groupMsg = req.data;
                if(store.state.tesssionid){
                    that.notLogin = true
                }else {
                    that.notLogin = false
                }
                }).catch(function (err) {
                    console.log(err)
                });
            if(category == ''){
                that.number = 1
            }else if(category == 'Python Web开发'){
                that.number = 2
            }else if(category == '网络爬虫'){
                that.number = 3
            }else if(category == '云计算与数据分析'){
                that.number = 4
            }else if(category == '人工智能'){
                that.number = 5
            }
        },
        showname(){
            return store.commit('showname')
        },
        groupOrder(order){
            let that = this;
            axios.get('/groups/?o='+order+"&c="+that.category,{
            }).then(function (req) {
                that.groupMsg = req.data;
            }).catch(function (err) {
                console.log(err)
            });
            if(order == 'new'){
                that.hotnumber = true
            }else{
                that.hotnumber = false
            }
        },
        hottGroup(order){
            let that = this;
            axios.get('/groups/?o='+ order +'&limit=5',{
            }).then(function (req) {
                that.hotGroup = req.data;
            }).catch(function (err) {
                console.log(err)
            })
        },
        showJoin:function(id){
            this.showDialog = "inline-block";
            this.groupId = id;
        },
        hideJoin(){
            this.showDialog = "none"
        },
        joinGroup(n){
            let that = this;
            tesessionid = this.$cookies.get('tesssionid');
            if(tesessionid == null){
                location.href = '../../login.html'
            }
            axios.post("/groups/"+n+"/members/",{
                "apply_reason":that.apply_reason,
            },{
                headers:{
                    tsessionid:tesessionid
                }
            }).then((req)=>{
                console.log(req.data)
                alert('加入小组成功！')
                location.href = '../../html/group/group.html'
            }).catch((err)=>{
                console.log(err);
                    if(err.response.status === 400){
                        if(err.response.data.non_fields){
                            alert(err.response.data.non_fields)
                        }
                    }
            })
        }
    }
});

