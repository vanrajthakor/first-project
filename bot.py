import telebot
import time
from models import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
import os
from datetime import date
from telebot.apihelper import ApiException

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

token="942272706:AAH96_s6ePwNCoEfRCCDcPub0ywlwG9n3jg"
bot=telebot.TeleBot(token)
admin=[635256922]
group="@PinkPromotion"
channel="@PinkPromotionDaily"


def user_data(message):
    user=session.query(User).filter(User.chat_id == message.chat.id).all()
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.chat.id
    
    if first_name == None:
        first_name = 'None'
    if last_name == None:
        last_name = 'None'
    if username == None:
        username = 'None'
    if chat_id == None:
        chat_id = 'None'
    
    if not len(user):
        session.add(User(chat_id=message.chat.id,username=username,first_name=first_name,last_name=last_name))
        session.commit()
    if len(user):
        session.query(User).filter(User.chat_id == message.from_user.id).update({User.first_name:first_name,User.last_name:last_name,User.username:username},synchronize_session='fetch')
        #session.query(User).filter(User.chat_id == message.from_user.id).update({User.last_name:last_name},synchronize_session='fetch')
        #session.query(User).filter(User.chat_id == message.from_user.id).update({User.username:username},synchronize_session='fetch')
        session.commit()
    
def channel_data(message):
    channel=session.query(Channel).filter(Channel.channel_id == message.forward_from_chat.id).all()
    channel_name= message.forward_from_chat.title
    channel_username=message.forward_from_chat.username
    channel_id=message.forward_from_chat.id
    chat_id = message.chat.id
    subscribers=bot.get_chat_members_count(str(message.forward_from_chat.id))
    admin_username=message.from_user.username
    
    if channel_name == None:
        channel_name = 'None'
    if channel_id==None:
        channel_id='None'
    if chat_id == None:
        chat_id = 'None'
    if subscribers==None:
        subscribers='None'

    if not len(channel):
        session.add(Channel(chat_id=message.chat.id,channel='@'+channel_username,channel_id=channel_id,subscribers=subscribers,admin_username='@'+admin_username,channel_name=channel_name))
        session.commit()
        get_=bot.send_message(message.chat.id,"✅ Send description(max 5 words and 2 emojis)",parse_mode='markdown')
	text_k = "Ok files"
        bot.register_next_step_handler(get_,add_description,channel_id)
        
    if len(channel):
        bot.send_message(message.chat.id,"Channel Already Exist",reply_markup=channel_markup())
        #session.query(User).filter(User.chat_id == message.from_user.id).update({User.last_name:last_name},synchronize_session='fetch')
        #session.query(User).filter(User.chat_id == message.from_user.id).update({User.username:username},synchronize_session='fetch')
        session.commit()

def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    add_channel=InlineKeyboardButton('➕ Add your Channel',callback_data='add_channel')
    my_channel=InlineKeyboardButton('🏷 My Channels',callback_data='my_channel')
    share=InlineKeyboardButton('🌐 Share Bot',switch_inline_query=' Pink Promotion provides you the best cross promotion services! Add your channel and Participate in Promotions Join Now @Apkkkkkbot')
    helpn=InlineKeyboardButton('🆘 Help',callback_data='help')
    markup.add(add_channel)
    markup.add(my_channel)
    markup.add(helpn,share)
    return markup
@bot.message_handler(commands=['check'])
def private_channel():
	privvate = message.text + "This is your text"
	bot.reply_to(message, privvate)
	
	
def done_channel_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    add_channel=InlineKeyboardButton('➕ Add Channel',callback_data='add_channel')
    my_channel=InlineKeyboardButton('🏷 My Channels',callback_data='my_channel')
    markup.add(add_channel)
    markup.add(my_channel)
    
    return markup

def channel_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    done=InlineKeyboardButton('➕ Add Channel',callback_data='add_channel')
    markup.add(done)
    return markup

def my_channel_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    done=InlineKeyboardButton('➕ Add Channel',callback_data='add_channel')
    remove=InlineKeyboardButton('🗑 Remove Channel',callback_data='remove_channel')
    markup.add(done,remove)
    return markup

def help_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    admin=InlineKeyboardButton('👨🏻‍💼 Contact Admin',url='https://t.me/PinkPromotionAdmin')
    dev=InlineKeyboardButton('👨🏻‍💻 Contact Developer',url='https://t.me/PinkPromotionAdmin')
    markup.add(admin)
    markup.add(dev)
    return markup

def contact_admin_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    admin=InlineKeyboardButton('👨🏻‍💼 Contact Admin',url='https://t.me/PinkPromotionAdmin')
    markup.add(admin)
    return markup

@bot.message_handler(commands=['start'])
def start_handler(msg): 
    bot.send_chat_action(msg.chat.id,'typing')
    bot.send_message(msg.chat.id,'Hello *{0.first_name}*👋🏻\n'.format(msg.from_user),parse_mode='Markdown',reply_markup=start_markup())  
    user_data(msg)

@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):
    if call.data=='add_channel':
        sent=bot.send_message(call.from_user.id, "✅ *Make the bot admin and Forward the message from Channel*",parse_mode='Markdown')
        bot.register_next_step_handler(sent,add_channel_name)

    if call.data=='my_channel':
        us='_________________________________________________________'
        cid=str(call.message.chat.id)
        try:
            f=open('user.txt','r').read()
            m=""
            if cid in f:
                a=session.query(Channel).filter(Channel.chat_id==call.from_user.id)
                b=session.query(Channel).filter(Channel.chat_id==call.from_user.id).all()
                
                for i in b:
                    m+=str(i)+'\n'+us+'\n'
                bot.send_message(call.message.chat.id,f'➖Total Channels : {a.count()}\n\n{m}',reply_markup=my_channel_markup())
            else:
                bot.send_message(call.message.chat.id,"⚠️ *You haven't registered any channel with our bot yet Or Channels might have been removed or banned*",parse_mode='Markdown',reply_markup=channel_markup())
        except Exception:
            pass

    if call.data=='remove_channel':
        s=bot.send_message(call.message.chat.id,"✅ *Send the Channel username*",parse_mode='Markdown')
        bot.register_next_step_handler(s,remove)
    
    if call.data=='help':
        a=f"◼️*Promotion Rules*\n*───────────*\n\n➤ 1 hour on Top.\n➤ 24 hours in the channel.\n➤ Don't Delete The List Before 24 hours otherwise you will be punished\n if you want to get unban then share list again with duration Of 3 Hours on top\n\n🚫 Those who break the rules will be banned."
        bot.send_message(call.message.chat.id,a,parse_mode="markdown",reply_markup=help_markup())

    if call.data=='announce':
        if call.message.chat.id in admin:
            sent=bot.send_message(call.from_user.id, "✅ Choose Announcement Category",reply_markup=announce_markup())
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    if call.data=='mail':
        if call.message.chat.id in admin:
            sent=bot.send_message(call.message.chat.id,'Enter the Message',reply_markup=back_markup())
            bot.register_next_step_handler(sent,mail)
    
    if call.data=='open_reg':
        if call.message.chat.id in admin:
            grp_reg_message=f"🔰 Registration Started 🔰 \n\n➖ Participation Method\n1. [Click Here To Participate](https://t.me/PinkPromotion)\n2. Click on start\n3. Click ‘My Channels’ to check your registred channels\n4. New members, this is one time registration. You don't need to register your channel for next promo\n5. Old members, we will update Channel subs count via bot. Do not worry about subscribers count. Make sure you have public channel."
            grp_reg_message1=f'✅ List Rules\n- 2 Hours Top\n- 2 Days in Channel\n- 24 Hours to Share\n————————————\n⚠️ List Type Promotion'
            grp_reg_message2=f'{grp_reg_message}\n\n{grp_reg_message1}'
            bot.send_message(group,grp_reg_message2,parse_mode='markdown')
            user_reg_message=f'ℹ️ Admin notification\n\n✅ Registration has been started\n\n*List Rules*\n1. 2 Hours on 🔝 In channel \n2. 2 Days in Channel\n3. 24 Hours To Share\n\n[Click to Participate](https://t.me/PinkPromotion1KBot?start)'
            for user in session.query(User):
                try:
                    bot.send_message(user.chat_id,user_reg_message,parse_mode='markdown')
                except Exception:
                    pass
            bot.send_message(call.message.chat.id,'☑️Done!')
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    if call.data=='close_reg':
        if call.message.chat.id in admin:
            a=session.query(Channel.id)
            m=f'🔰Registration has been closed\n\n- List will be out soon.\n- Stay tuned!\n\n*Total Channel Registered :* {a.count()}'
            bot.send_message(group,m,parse_mode='markdown')
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=="list_out":
        if call.message.chat.id in admin:
            try:
                f=open("save.txt","r",encoding='utf-8').read()
                user_message="ℹ️ Admin notification\n\n✅ List is out \nhttp://t.me/PinkPromotionDaily/"+f+"\n\nList Rules\n1. 2 Hours on 🔝 In channel \n2. 2 Days in Channel \n3. 24 Hours To Share'\n\n"
                for user in session.query(User):
                    try:
                        bot.send_message(user.chat_id,user_message,parse_mode='markdown')
                    except Exception:
                        pass
                bot.send_message(call.message.chat.id,'☑️Done!')
            except Exception:
                bot.send_message(call.message.chat.id,"⚠️ NOT FOUND")
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
        


    if call.data=='ban':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"✅ Send Channel Username ",reply_markup=back_markup())
            bot.register_next_step_handler(a,aban)
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='unban':
        if call.message.chat.id in admin:
            b=bot.send_message(call.message.chat.id,"✅ Send Channel Username ",reply_markup=back_markup())
            bot.register_next_step_handler(b,unban)
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
        
    if call.data=='back':
        bot.delete_message(call.message.chat.id,call.message.message_id)
        
    if call.data=='update_subs':
        if call.message.chat.id in admin:
            subs=session.query(Channel).all()
            for update in subs:
                print(update.channel)
                up=bot.get_chat_members_count(update.channel)
                session.query(Channel).filter(Channel.channel==update.channel).update({Channel.subscribers:up})
                session.commit()
            bot.send_message(call.message.chat.id,"✅ Updated Succesfully")
        else :
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    
    if call.data=="show_channel":
        if call.message.chat.id in admin:
            
                c=bot.send_message(call.message.chat.id,"✅ Send Channel Username ",reply_markup=back_markup())
                bot.register_next_step_handler(c,showchannel)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='list':
        if call.message.chat.id in admin:
            bot.send_message(call.message.chat.id,"☑️ Choose Required List",reply_markup=list_markup())
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='ban_list':
        if call.message.chat.id in admin:
            val=""
            a=session.query(Ban).all()
            count=session.query(Ban).count()
            for i in a:
                val+=str(i)+'\n'
            l=f'Total Banned Channels : {count}\n\n{val}'
            bot.send_message(call.message.chat.id,l)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='channel_list':
        if call.message.chat.id in admin:
            val=""
            a=session.query(Channel).all()
            count=session.query(Channel).count()
            for i in a:
                val+=str(i.id)+'. '+str(i.channel)+'\n'
            l=f'Total Channels : {count}\n\n{val}'
            bot.send_message(call.message.chat.id,l)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    
    if call.data=='user_list':
        if call.message.chat.id in admin:
            val=""
            a=session.query(User).all()
            count=session.query(User).count()
            for i in a:
                c=session.query(Channel).filter(Channel.admin_username=='@'+i.username).count()
                val+=str(i.id)+'. @'+str(i.username)+' ('+str(c)+')'+'\n'
            l=f'Total User : {count}\n\n{val}'
            bot.send_message(call.message.chat.id,l)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    
    if call.data=='stats':
        if call.message.chat.id in admin:
            ban=session.query(Ban).count()
            channel=session.query(Channel).count()
            user=session.query(User).count()
            stats=f'*Users :* {user}\n*Registerd Channels :* {channel}\n*Banned Channels :* {ban}'
            bot.send_message(call.message.chat.id,stats,parse_mode='markdown')
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='create_post':
        if call.message.chat.id in admin:
            bot.send_message(call.message.chat.id,"✅ Set Required Field",reply_markup=create_post_markup())
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='emoji':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"*✅ Send Emoji Now*",parse_mode='markdown',reply_markup=back_markup())
            bot.register_next_step_handler(a,emoji)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='top_sponser':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"*✅ Send Text With Parse mode(if required)*",parse_mode='markdown',reply_markup=back_markup())
            bot.register_next_step_handler(a,top_text)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
        
    if call.data=='bottom_sponser':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"*✅ Send Text With Parse mode(if required)*",parse_mode='markdown',reply_markup=back_markup())
            bot.register_next_step_handler(a,bottom_text)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='set_button':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"*✅ Send Text for Button *",parse_mode='markdown',reply_markup=back_markup())
            bot.register_next_step_handler(a,button_text)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='set_caption':
        if call.message.chat.id in admin:
            a=bot.send_message(call.message.chat.id,"*✅ Send Caption (Button Promo)*",parse_mode='markdown',reply_markup=back_markup())
            bot.register_next_step_handler(a,set_cap)
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')
    if call.data=='dlt_button':
        try:
            session.query(Button).delete()
            session.commit()
            bot.send_message(call.message.chat.id,"✅ Done")
        except Exception:
            bot.send_message(call.message.chat.id,"No Data Found")

    if call.data=='preview':
        if call.message.chat.id in admin:
            bot.send_message(call.message.chat.id,"✅ Choose Promo List",reply_markup=promo_markup())
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='button_promo':
        try:
            c=session.query(Post.set_caption).first()
            bot.send_photo(call.message.chat.id,open('a.jpg','rb'),caption=c,reply_markup=button_markup(),parse_mode='HTML')
        except Exception:
            bot.send_message(call.message.chat.id,"*⚠️ Please Set Caption *",parse_mode='markdown',reply_markup=set_cap_markup())

    if call.data=='classic_promo':
        try:
            a=session.query(Channel).all()
            b=session.query(Post).first()
            val=""
            p="🗣Via @PinkPromotion\n1 hr 🕐Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='http://t.me/PPPaidPromotion'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"
            for i in a:
                val+=b.emoji+str(i.channel)+'\n'
            dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
            bot.send_message(call.message.chat.id,dest,reply_markup=promo_button_markup(),disable_web_page_preview=True,parse_mode='HTML')
        except Exception:
            bot.send_message(call.message.chat.id,"*⚠️ Please Set Required *",parse_mode='markdown',reply_markup=set_markup())

    if call.data=='morden_promo':
        try:
            a=session.query(Channel).all()
            b=session.query(Post).first()
            val=""
            p="🗣Via @PinkPromotion\n1 hr 🕐Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='http://t.me/PPPaidPromotion'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"
            for i in a:
                val+='<b>'+str(i.description)+'</b>'+"\n"+b.emoji+'<a href="http://t.me/'+str(i.channel).replace('@'," ")+'">「Joιɴ Uѕ」</a>'+b.emoji+'\n\n'
            dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
            bot.send_message(call.message.chat.id,dest,reply_markup=promo_button_markup(),parse_mode='HTML',disable_web_page_preview=True)
        except Exception:
            bot.send_message(call.message.chat.id,"*⚠️ Please Set Required *",parse_mode='markdown',reply_markup=set_markup())
    
    if call.data=='send_promo':
        if call.message.chat.id in admin:
            bot.send_message(call.message.chat.id,"✅ *Choose Promo List*",parse_mode='markdown',reply_markup=send_promo_markup())
        else:
            bot.send_message(call.message.chat.id,'*This access only for admin*',parse_mode='markdown')

    if call.data=='dlt_promo':
        ch=""
        try:
            a=session.query(Promo).all()
            for i in a:
                try:
                    bot.delete_message(i.channel,i.message_id)
                except ApiException:
                    z="🚫 Message delete Unsucessful\n"
                    ch+=i.channel+'\n'
            bot.send_message(call.message.chat.id,"✅ DONE")
            try:
                bot.send_message(call.message.chat.id,z+ch)
            except Exception :
                pass
        except Exception:
            pass



    if call.data=="send_morden_promo":
        try:
            a=session.query(Channel).all()
            b=session.query(Post).first()
            val=""
            p="🗣Via @PinkPromotion\n1 hr 🕐Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='http://t.me/PPPaidPromotion'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"
            for i in a:
                val+='<b>'+str(i.description)+'</b>'+"\n"+b.emoji+'<a href="http://t.me/'+str(i.channel).replace('@',"")+'">「Join Us」</a>'+b.emoji+'\n\n'
            dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
            us='*___________________________*'
            channl=""
            unsucess=""
            qe=bot.send_message("@PinkPromotion",dest,reply_markup=promo_button_markup(),parse_mode='HTML',disable_web_page_preview=True)
            f=open("save.txt","w")
            f.write(str(qe.message_id))
            f.close()
            
            for j in a:
                try:
                    mes=bot.send_message(j.channel,dest,reply_markup=promo_button_markup(),parse_mode='HTML',disable_web_page_preview=True)
                    
                    promo=session.query(Promo).filter(Promo.channel ==j.channel).all()
                    if not len(promo):
                        session.add(Promo(channel=j.channel,message_id=mes.message_id))
                        session.commit()
                    
                    if len(promo):
                        session.query(Promo).filter(Promo.channel ==j.channel).update({Promo.message_id:mes.message_id})
                        session.commit()
                    zx=session.query(Promo).filter(Promo.channel==j.channel).first()
                    channl+="✅ Channel :" +j.channel+'\n'+"http://t.me/"+j.channel+'/'+str(zx.message_id)+"\n"+us+"\n\n"
                    cg="#shared Successful\n\n"
                except ApiException:
                        dg="#shared Unsucessful\n\n"
                        unsucess+="🚫 "+j.channel+'\n'
            try:
                bot.send_message(group,cg+channl,parse_mode='markdown')
            except Exception :
                pass
            try:
                bot.send_message(group,dg+unsucess)
            except Exception:
                pass
            bot.send_message(call.message.chat.id,"✅ DONE")
        except ApiException:
            pass
        except Exception:
            bot.send_message(call.message.chat.id,"*⚠️ Please Set Required *",parse_mode='markdown',reply_markup=set_markup())

    if call.data=="send_button_promo":
        try:
            a=session.query(Channel).all()
            b=session.query(Post).first()
            channl=""
            unsucess=""
            us='*___________________________*'
            qe=bot.send_photo("@PinkPromotion",open('a.jpg','rb'),caption=b.set_caption,reply_markup=button_markup(),parse_mode='HTML')
            f=open("save.txt","w")
            f.write(str(qe.message_id))
            f.close()
            for i in a:
                try:
                    cg="#shared Successful\n\n"
                    mes=bot.send_photo(i.channel,open('a.jpg','rb'),caption=b.set_caption,reply_markup=button_markup(),parse_mode='HTML')
                    promo=session.query(Promo).filter(Promo.channel ==i.channel).all()
                    if not len(promo):
                        session.add(Promo(channel=i.channel,message_id=mes.message_id))
                        session.commit()
                    if len(promo):
                        session.query(Promo).filter(Promo.channel ==i.channel).update({Promo.message_id:mes.message_id})
                        session.commit()
                    zx=session.query(Promo).filter(Promo.channel==i.channel).first()
                    channl+="✅ Channel :" +i.channel+'\n'+"http://t.me/"+i.channel+'/'+str(zx.message_id)+"\n"+us+"\n\n"
                except ApiException:
                        dg="#shared Unsucessful\n\n"
                        unsucess+="🚫 "+i.channel+'\n'
            try:
                bot.send_message(group,cg+channl,parse_mode='markdown')
            except Exception :
                pass
            try:
                bot.send_message(group,dg+unsucess)
            except Exception :
                pass
            bot.send_message(call.message.chat.id,"✅ DONE")
        except ApiException:
            pass
        except Exception:
           bot.send_message(call.message.chat.id,"*⚠️ Please Set Caption *",parse_mode='markdown',reply_markup=set_cap_markup())
    
    if call.data=='send_classic_promo':
        try:
            a=session.query(Channel).all()
            b=session.query(Post).first()
            val=""
            p="🗣Via @PinkPromotion\n1 hr 🕐Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='http://t.me/PPPaidPromotion'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"
            for i in a:
                val+=b.emoji+str(i.channel)+'\n'
            dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
            us='*___________________________*'
            channl=""
            unsucess=""
            qe=bot.send_message("@PinkPromotion",dest,reply_markup=promo_button_markup(),parse_mode='HTML',disable_web_page_preview=True)
            f=open("save.txt","w")
            f.write(str(qe.message_id))
            f.close()
            for j in a:
                try:
                    mes=bot.send_message(j.channel,dest,reply_markup=promo_button_markup(),parse_mode='HTML',disable_web_page_preview=True)
                    
                    promo=session.query(Promo).filter(Promo.channel ==j.channel).all()
                    if not len(promo):
                        session.add(Promo(channel=j.channel,message_id=mes.message_id))
                        session.commit()
                    
                    if len(promo):
                        session.query(Promo).filter(Promo.channel ==j.channel).update({Promo.message_id:mes.message_id})
                        session.commit()
                    zx=session.query(Promo).filter(Promo.channel==j.channel).first()
                    channl+="✅ Channel :" +j.channel+'\n'+"http://t.me/"+j.channel+'/'+str(zx.message_id)+"\n"+us+"\n\n"
                    cg="#shared Successful\n\n"
                except ApiException:
                        dg="#shared Unsucessful\n\n"
                        unsucess+="🚫 "+j.channel+'\n'
            try:
                bot.send_message(group,cg+channl,parse_mode='markdown')
            except Exception :
                pass
            try:
                bot.send_message(group,dg+unsucess)
            except Exception:
                pass
        except ApiException:
            pass
            
        except Exception:
            bot.send_message(call.message.chat.id,"*⚠️ Please Set Required *",parse_mode='markdown',reply_markup=set_markup())
    

def set_cap(message):
    post=session.query(Post).filter(Post.chat_id == message.chat.id).all()
    if not len(post):
        session.add(Post(chat_id=message.chat.id,set_caption=message.text))
        session.commit()
    if len(post):
        session.query(Post).filter(Post.chat_id==message.chat.id).update({Post.set_caption:message.text})
        session.commit()
    bot.send_message(message.chat.id,"➖ Top Text Successfully Set")

def button_text(message):
    message_button=message.text
    session.add(Button(chat_id=message.chat.id,set_button_name=message.text))
    session.commit()
    a=bot.send_message(message.chat.id,"*✅ Send Link for Button *",parse_mode='markdown')
    bot.register_next_step_handler(a,button_link,message_button)

def button_link(message,message_button):
    link=message.text
    session.query(Button).filter(Button.set_button_name==message_button).update({Button.set_button_url:link})
    session.commit()
    bot.send_message(message.chat.id,"*✅ Button added Sucessfully*",parse_mode='markdown')

def bottom_text(message):

    post=session.query(Post).filter(Post.chat_id == message.chat.id).all()
    if not len(post):
        session.add(Post(chat_id=message.chat.id,set_bottom=message.text))
        session.commit()
    if len(post):
        session.query(Post).filter(Post.chat_id==message.chat.id).update({Post.set_bottom:message.text})
        session.commit()
    bot.send_message(message.chat.id,"Bottom Text Successfully Set")
    a=session.query(Post).first()
    bot.send_message(message.chat.id,str(a.set_bottom),parse_mode="HTML")

def top_text(message):
    post=session.query(Post).filter(Post.chat_id == message.chat.id).all()
    if not len(post):
        session.add(Post(chat_id=message.chat.id,set_top=message.text))
        session.commit()
    if len(post):
        session.query(Post).filter(Post.chat_id==message.chat.id).update({Post.set_top:message.text})
        session.commit()
    bot.send_message(message.chat.id,"Top Text Successfully Set")
    a=session.query(Post.set_top).first()
    bot.send_message(message.chat.id,a,parse_mode='HTML')

def emoji(message):
    post=session.query(Post).filter(Post.chat_id == message.chat.id).all()
    if not len(post):
        session.add(Post(chat_id=message.chat.id,emoji=message.text))
        session.commit()
    if len(post):
        session.query(Post).filter(Post.chat_id==message.chat.id).update({Post.emoji:message.text})
        session.commit()
    bot.send_message(message.chat.id,"Emoji Successfully Set")

            
def showchannel(message):
    if message.chat.id in admin:
        username=message.text
        try:
            a=session.query(Channel).filter(Channel.channel==message.text).first()
            deatils=f'⚠️ Channel ID : {a.channel_id}\n🔺 Channel name : {a.channel_name}\n✅ Subscribers : {a.subscribers}\n➖ Admin ID : {a.chat_id}\n🏷  Admin : {a.admin_username}'
            bot.send_message(message.chat.id,deatils)
        except Exception:
                bot.send_message(message.chat.id,"❌ Data Not found")
    else:  
        bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')

def aban(message):
    username=message.text
    try:
        z=session.query(Channel).filter(Channel.channel==message.text).first() 
        print(z.channel)
        session.add(Ban(username=z.channel))
        bot.send_message(z.chat_id,"🚫 Your Channel is banned",reply_markup=contact_admin_markup())
        session.query(Channel).filter(Channel.channel==message.text).delete()
        session.commit()
        bot.send_message(message.chat.id,f'{message.text} Banned ')
    except Exception:
        bot.send_message(message.chat.id,"No Channel Found..!")

def unban(message):
    u=message.text
    try:
        session.query(Ban).filter(Ban.username==u).delete()
        session.commit()
        bot.send_message(message.chat.id,"✅ Done")
    except Exception:
        bot.send_message(message.chat.id,"No Data Found")

def mail(message):
    chat_id = message.chat.id
    
    if chat_id in admin:
        for user in session.query(User):
            try:
                bot.send_message(user.chat_id,message.text)
            except Exception:
                pass
        bot.send_message(message.chat.id,'☑️Mailing finished!')
    else :
            bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')

def add_channel_name(message):
    try:
        username=f'@{message.forward_from_chat.username}'
        ban=session.query(Ban).filter(Ban.username==username).first()
        try:
            f=open('ban.txt','w')
            f.write(ban.username)
            f.close()
            r=open('ban.txt','r').read()
            if username in r:
                bot.send_message(message.chat.id,"This Channel is Banned ",reply_markup=contact_admin_markup())
                
        except Exception:
            try:
                bot.get_chat(message.forward_from_chat.id)
                a=bot.get_chat_member(message.forward_from_chat.id,942272706)
                if a.status =='administrator':
                    member=bot.get_chat_members_count(str(message.forward_from_chat.id))
                    if member>=1:
                        channel_data(message)  
                    else:
                        bot.send_message(message.chat.id,"Minimum 1000 needed for Register")
                        
                else:
                    bot.send_message(message.chat.id,"*❌ Bot is not admin*",parse_mode='markdown')
            except Exception:
                bot.send_message(message.chat.id,"*❌ Bot is not admin*",parse_mode='markdown')
    except Exception:
        bot.send_message(message.chat.id,"⚠️ Channel not found")

def add_description(message,channel_id):
    session.query(Channel).filter(Channel.channel_id == channel_id).update({Channel.description:str(message.text)})
    session.commit()
    info=session.query(Channel).filter(Channel.channel_id == channel_id).first()
    details=f'✅ Channel Submitted Sucessfully\n\nChannel ID : {info.channel_id}\nChannel name :{info.channel_name}\nUsername : {info.channel}\nSubscribers : {info.subscribers}\nDescription : {info.description}'         
    bot.send_message(message.chat.id,details,reply_markup=done_channel_markup())
    send_group=f'✅ New Channel Submited!\nChannel ID : {info.channel_id}\nChannel name :{info.channel_name}\nUsername : {info.channel}\nSubscribers : {info.subscribers}\nDescription : {info.description}\nSubmitted By : {info.admin_username}'
    bot.send_message(group,send_group)
    f=open('user.txt','a')
    f.write(str(info.chat_id)+'\n')

def remove(message):
    session.query(Channel).filter(Channel.channel==message.text).delete()
    session.commit()
    bot.send_message(message.chat.id,"Channel Removed")

#Admin panel
def button_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    a=session.query(Channel).all()
    for i in a:
        m=InlineKeyboardButton(i.description,url='https://t.me/'+i.channel.replace('@',''))
        markup.add(m)
    b=session.query(Button).all()
    for j in b:
        n=InlineKeyboardButton(j.set_button_name,url=j.set_button_url)
        markup.add(n)
    return markup

def admin_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    announce=InlineKeyboardButton('📢 Announcement',callback_data='announce')
    mail=InlineKeyboardButton('📤 Mailing',callback_data='mail')
    ban=InlineKeyboardButton('🚫 Ban Channel',callback_data='ban')
    unban=InlineKeyboardButton('📍 Unban Channel',callback_data='unban')
    update_subs=InlineKeyboardButton('🔄 Update Subscribers',callback_data='update_subs')
    show_channel=InlineKeyboardButton('ℹ️ Channel Info',callback_data='show_channel')
    bot_support=InlineKeyboardButton('⚙ Bot Support',url='https://t.me/joinchat/GbIvzxMleRp7WCliVG7q2w')
    contact_dev=InlineKeyboardButton('👨🏻‍💻 Contact Dev',url='https://t.me/Bhosadiwale_Chacha')
    manage=InlineKeyboardButton('📊 Statistics',callback_data='stats')
    manage_list=InlineKeyboardButton('☑️ Manage List',callback_data='list')
    create_post=InlineKeyboardButton('📝 Create Post',callback_data='create_post')
    preview_list=InlineKeyboardButton('⏮ Preview List',callback_data='preview')
    send_promo=InlineKeyboardButton('✔️ Send Promo',callback_data='send_promo')
    dlt_promo=InlineKeyboardButton('✖️ Delete Promo',callback_data='dlt_promo')
    bot_doc=InlineKeyboardButton('📄 Bot Documentation',url='https://telegra.ph/DOCUMENTATION-CROSS-PROMOTE-BOT-06-27')
    markup.add(mail,announce)
    markup.add(ban,unban)
    markup.add(update_subs)
    markup.add(show_channel,manage_list)
    markup.add(manage,create_post)
    markup.add(preview_list)
    markup.add(send_promo,dlt_promo)
    markup.add(bot_support,contact_dev)
    markup.add(bot_doc)
    return markup

def create_post_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    top_sponser=InlineKeyboardButton('⬆️ Set Top Text',callback_data='top_sponser')
    bottom_sponser=InlineKeyboardButton('⬇️ Set Bottom Text',callback_data='bottom_sponser')
    emoji=InlineKeyboardButton('☑️ Set Emoji',callback_data='emoji')
    list_order=InlineKeyboardButton('🔘 Set Buttons',callback_data='set_button')
    delete_button=InlineKeyboardButton('🗑 Delete Buttons',callback_data='dlt_button')
    set_caption=InlineKeyboardButton('🔖 Set Caption',callback_data='set_caption')
    back=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(list_order,emoji)
    markup.add(top_sponser,bottom_sponser) 
    markup.add(set_caption,delete_button)
    markup.add(back)
    return markup

def promo_button_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    b=session.query(Button).all()
    for j in b:
        n=InlineKeyboardButton(j.set_button_name,url=j.set_button_url)
        markup.add(n)
    return markup    

def set_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    top_sponser=InlineKeyboardButton('⬆️ Set Top Text',callback_data='top_sponser')
    bottom_sponser=InlineKeyboardButton('⬇️ Set Bottom Text',callback_data='bottom_sponser')
    emoji=InlineKeyboardButton('☑️ Set Emoji',callback_data='emoji')
    markup.add(emoji)
    markup.add(top_sponser,bottom_sponser) 
    return markup

def set_cap_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    top_sponser=InlineKeyboardButton('🔖 Set Caption',callback_data='set_caption')
    markup.add(top_sponser)
    return markup

def promo_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    button_promo=InlineKeyboardButton('🔳 Button Promo',callback_data='button_promo')
    classic_promo=InlineKeyboardButton('🏛 Classic Promo',callback_data='classic_promo')
    morden_promo=InlineKeyboardButton('🔰 Standard Promo',callback_data='morden_promo')
    back=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(button_promo,classic_promo)
    markup.add(morden_promo)
    markup.add(back)
    return markup

def send_promo_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    button_promo=InlineKeyboardButton('🔳 Button Promo',callback_data='send_button_promo')
    classic_promo=InlineKeyboardButton('🏛 Classic Promo',callback_data='send_classic_promo')
    morden_promo=InlineKeyboardButton('🔰 Standard Promo',callback_data='send_morden_promo')
    back=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(button_promo,classic_promo)
    markup.add(morden_promo)
    markup.add(back)
    return markup

def list_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    channel_list=InlineKeyboardButton('🕹 Channel List',callback_data='channel_list')
    ban_list=InlineKeyboardButton('🚫 Ban List',callback_data='ban_list')
    user_list=InlineKeyboardButton('👤 User List',callback_data='user_list')
    back=InlineKeyboardButton('🔙 Back',callback_data='back')    
    markup.add(channel_list,ban_list)
    markup.add(user_list)
    markup.add(back)
    return markup

def announce_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    open_reg=InlineKeyboardButton('📖 Open Registration',callback_data='open_reg')
    close_reg=InlineKeyboardButton('📕 Close Registration',callback_data='close_reg')
    list_out=InlineKeyboardButton('📰 List Out Notification',callback_data='list_out')
    back=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(open_reg,close_reg)
    markup.add(list_out)
    markup.add(back)
    return markup

def back_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    back=InlineKeyboardButton('🔙 Back',callback_data='back')
    markup.add(back)
    return markup

@bot.message_handler(commands=['admin_start'])
def admin_start_handler(message): 
    if message.chat.id in admin:
        bot.send_message(message.chat.id,"✅ You logged in as Admin",reply_markup=admin_markup())
    else :
            bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')

while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		time.sleep(1)
