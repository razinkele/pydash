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

        // Update sidebar menu: payload {items: [{text: 'Home', href: '#'}]}
        Shiny.addCustomMessageHandler('bs4dash_update_sidebar', function(msg){
            try{
                var items = (msg && msg.items) ? msg.items : [];
                var nav = document.querySelector('.main-sidebar .nav');
                if(!nav) return;
                nav.innerHTML = '';
                items.forEach(function(it){
                    var li = document.createElement('li');
                    li.className = 'nav-item';
                    var a = document.createElement('a');
                    a.className = 'nav-link';
                    a.href = it.href || '#';
                    a.textContent = it.text || '';
                    li.appendChild(a);
                    nav.appendChild(li);
                });
            }catch(e){console.error(e);}
        });

        // Update nav tabs: payload {nav_id: 'some-id', tabs: [{id, title, href, active}]}
        Shiny.addCustomMessageHandler('bs4dash_update_navs', function(msg){
            try{
                var nav = document.getElementById(msg.nav_id);
                if(!nav) return;
                var tabs = msg.tabs || [];
                // replace inner ul of nav
                var ul = nav.querySelector('ul');
                if(!ul) return;
                ul.innerHTML = '';
                tabs.forEach(function(t){
                    var li = document.createElement('li');
                    li.className = 'nav-item';
                    var a = document.createElement('a');
                    a.className = 'nav-link' + (t.active ? ' active' : '');
                    a.href = t.href || '#';
                    a.textContent = t.title || '';
                    li.appendChild(a);
                    ul.appendChild(li);
                });
            }catch(e){console.error(e);}
        });

        // Update sidebar badges: payload {badges: [{href: '#about', badge: '3'}]}
        Shiny.addCustomMessageHandler('bs4dash_update_sidebar_badges', function(msg){
            try{
                var badges = msg.badges || [];
                var nav = document.querySelector('.main-sidebar .nav');
                if(!nav) return;
                badges.forEach(function(b){
                    // find link by href
                    var sel = "a.nav-link[href='" + (b.href || "#") + "']";
                    var a = nav.querySelector(sel);
                    if(!a) return;
                    // find existing badge
                    var existing = a.querySelector('.badge');
                    if(b.badge === null || b.badge === undefined || b.badge === ''){
                        if(existing) existing.remove();
                        return;
                    }
                    if(!existing){
                        var span = document.createElement('span');
                        span.className = 'badge badge-info float-right';
                        span.textContent = b.badge;
                        a.appendChild(span);
                    } else {
                        existing.textContent = b.badge;
                    }
                });
            }catch(e){console.error(e);}
        });

        // Update nav items (replace) with optional badges: payload {nav_id: 'demo', items: [{title, href, badge}]}
        Shiny.addCustomMessageHandler('bs4dash_update_nav_items', function(msg){
            try{
                var nav = document.getElementById(msg.nav_id);
                if(!nav) return;
                var items = msg.items || [];
                var ul = nav.querySelector('ul');
                if(!ul) return;
                ul.innerHTML = '';
                items.forEach(function(it){
                    var li = document.createElement('li');
                    li.className = 'nav-item';
                    var a = document.createElement('a');
                    a.className = 'nav-link';
                    a.href = it.href || '#';
                    a.textContent = it.title || '';
                    if(it.badge){
                        var span = document.createElement('span');
                        span.className = 'badge badge-info float-right';
                        span.textContent = it.badge;
                        a.appendChild(span);
                    }
                    li.appendChild(a);
                    ul.appendChild(li);
                });
            }catch(e){console.error(e);}
        });

        // Update tab content: payload {tab_id: 't1', content: '<p>…</p>'}
        Shiny.addCustomMessageHandler('bs4dash_update_tab_content', function(msg){
            try{
                var el = document.getElementById(msg.tab_id);
                if(!el) return;
                el.innerHTML = msg.content || '';
            }catch(e){console.error(e);}
        });

        // Pushmenu toggle: click handler toggles `sidebar-collapse` on <body>
        try{
            var pm = document.getElementById('pushmenu-toggle');
            if(pm){
                pm.addEventListener('click', function(ev){
                    ev.preventDefault();
                    document.body.classList.toggle('sidebar-collapse');
                });
            }
        }catch(e){console.error(e);}

        // Controlbar toggle click handler: toggle control sidebar visibility
        try{
            var cb = document.getElementById('controlbar-toggle');
            if(cb){
                cb.addEventListener('click', function(ev){
                    ev.preventDefault();
                    document.body.classList.toggle('control-sidebar-open');
                });
            }
        }catch(e){console.error(e);}
    }
})();
