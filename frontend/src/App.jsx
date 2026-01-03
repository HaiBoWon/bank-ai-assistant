import React, { useState } from 'react'
import Chat, { Bubble, useMessages, Typing } from '@chatui/core'
import '@chatui/core/dist/index.css'
import axios from 'axios'
import './App.css'

const initialMessages = [
  {
    type: 'text',
    content: {
      text: '您好！我是银行智能客服助手，可以为您解答以下问题：\n\n• 账户类：挂失、余额查询、交易明细、冻结/解冻\n• 信用卡类：账单查询、还款、额度提升、逾期罚息、积分兑换\n• 基础业务类：手机银行/网银注册、转账限额、手续费、利率查询\n• 常见操作类：密码重置、短信提醒、银行卡解绑\n\n请问有什么可以帮助您的吗？',
    },
    user: {
      avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    },
  },
]

function App() {
  const { messages, appendMsg, deleteMsg } = useMessages(initialMessages)

  async function handleSend(type, val) {
    if (type === 'text' && val.trim()) {
      // 添加用户消息
      const userMsg = {
        type: 'text',
        content: { text: val },
        position: 'right',
        user: {
          avatar: 'https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg',
        },
      }
      appendMsg(userMsg)

      // 创建并添加typing消息
      const typingMsg = {
        type: 'typing',
        _id: `typing-${Date.now()}`,
        user: {
          avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
        },
      }
      appendMsg(typingMsg)

      try {
        // 调用后端 API，设置30秒超时
        const response = await axios.post(
          '/api/chat',
          {
            question: val,
          },
          {
            timeout: 30000, // 30秒超时
          }
        )

        const answer = response.data.answer
        const category = response.data.category
        const topic = response.data.topic

        // 格式化回答
        let formattedAnswer = answer
        if (topic) {
          formattedAnswer = `【${category} - ${topic}】\n\n${answer}`
        }

        // 添加机器人回复
        appendMsg({
          type: 'text',
          content: { text: formattedAnswer },
          user: {
            avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
          },
        })
      } catch (error) {
        console.error('API 调用失败:', error)
        let errorMessage = '抱歉，服务暂时不可用，请稍后重试。'
        
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
          errorMessage = '请求超时，请稍后重试。如果问题持续，建议联系人工客服（电话：95588）。'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.message) {
          errorMessage = `错误：${error.message}`
        }
        
        appendMsg({
          type: 'text',
          content: {
            text: errorMessage,
          },
          user: {
            avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
          },
        })
      } finally {
        // 移除typing消息
        deleteMsg(typingMsg._id)
      }
    }
  }

  function renderMessageContent(msg) {
    if (msg.type === 'typing') {
      // 只保留三个点的动画效果
      return (
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          padding: '10px',
          gap: '4px'
        }}>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            background: '#999', 
            animation: 'typing 1.4s infinite'
          }}></div>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            background: '#999', 
            animation: 'typing 1.4s infinite .2s'
          }}></div>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            background: '#999', 
            animation: 'typing 1.4s infinite .4s'
          }}></div>
        </div>
      )
    }
    const { content } = msg
    return <Bubble content={content.text} />
  }

  return (
    <div className="app-container">
      <Chat
        navbar={{
          desc: <div style={{color: '#fff', fontSize: '18px'}}>银行智能客服助手</div>,
        }}
        messages={messages}
        renderMessageContent={renderMessageContent}
        onSend={handleSend}
        placeholder="请输入您的问题..."
        toolbar={[]}
        locale="zh-CN"
      />
    </div>
  )
}

export default App

