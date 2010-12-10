<%inherit file="base.mako"/>
<p>
 To permanently delete your Firefox Sync account and all copies of your data stored on our servers, please enter your username and password and click Permanently Delete My Account.
</p>
 %if error:
 <div class="error">${error}</div>
 %endif
 <form class="mainForm" name="deleteAccount" id="deleteAccount"
    action="/weave-delete-account" method="post">
  <p>
  <label>Username:
    <input type="text" name="username" id="user_name" size="20"/>
   </label>
  </p>
  <label>Password:
    <input type="password" name="password" id="user_pass" size="20"/>
   </label>
  </p>

  <input type="submit" id="pchange" name="pchange"
         value="Permanently Delete My Account"/>
 </form>
</p>
