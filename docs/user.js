


class User{

    constructor(user,password){
        this._Password=password.toUpperCase();
        this._User=user.toUpperCase();
    }
    get User(){
        return this._User;
    }
    get Password(){
        return this._Password;
    }
    get UserData(){
        return {"user":this.User,"password":this.Password};
    }



    Login(){
        return User._DoIt(User.UrlLogin,this.UserData);
    }
    DownState(){
        return User._DoIt(User.UrlDownState,this.UserData);
    }
    UpState(){
        return User._DoIt(User.UrlUpState,this.UserData);
    }
    UpdateState(){
        return User._DoIt(User.UrlUpdateState,this.UserData);
    }

    static get UrlUpdateState(){
        return User.UrlFuncions+"/UpdateState";
    }
    static get UrlUpState(){
        return User.UrlFuncions+"/UpState";
    }
    static get UrlDownState(){
        return User.UrlFuncions+"/DownState";
    }
    static get UrlDardo(){
        return User.UrlFuncions+"/PeticioDardo.do";
    }
    static get UrlLogin(){
        return User.UrlFuncions+"/Check";

    }
    static get UrlFuncions(){
        return /*"http://192.168.0.19:5002";*/"http://tetradogbeta.ddns.net:5005";
    }

    static _DoIt(url,formData){
        return new Promise((resolver,rechazar)=>{
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url,true);
            xhr.setRequestHeader("Content-Type","application/json");
            xhr.onload=function(){
                var result;
                if(this.status==200){
                    result=JSON.parse(this.responseText);
                    if(!result.error){
                        resolver(result.result);
                    }else{
                        rechazar(result.result);
                    }
                }
                else{
                    rechazar(null);
                }
            };
            xhr.send(JSON.stringify(formData));
      

        });
    }



}