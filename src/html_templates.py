css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #260b7d;
    text-align: right;
}
.chat-message.bot {
    background-color: #300914
}
.chat-message .avatar {
  width: 10%;
}
.chat-message .avatar img {
  max-width: 100px;
  max-height: 100px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 90%;
  padding: 0 1.5rem;
  color: #dee0f1;
}

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://image.lexica.art/full_webp/1e13b417-57f1-4e2c-bb8f-36e3ba7a665e">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://avatars.githubusercontent.com/u/53319367?v=4">
    </div>    
</div>
'''
