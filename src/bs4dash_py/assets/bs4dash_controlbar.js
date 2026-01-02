(function(){
    function handle(msg){
        var action = msg && msg.action ? msg.action : 'toggle';
        var body = document.body;
        if(!body) return;
        if(action === 'show') body.classList.add('control-sidebar-open');
        else if(action === 'hide') body.classList.remove('control-sidebar-open');
        else body.classList.toggle('control-sidebar-open');
    }
    if(window.Shiny && Shiny.addCustomMessageHandler){
        Shiny.addCustomMessageHandler('bs4dash_controlbar', handle);
    }
})();
