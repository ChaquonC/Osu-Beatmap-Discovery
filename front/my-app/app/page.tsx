"use client"

import {useRef, useState} from "react"
import "./chat.css"

const api_base: string | undefined = process.env.NEXT_PUBLIC_BACKEND_API

type Message = {
    role: "user" | "assistant"
    content: string
}

type APIResponse = {
    status_code: number
    data: Message[]
}

export default function Page() {
    const [messages, setMessages] = useState<Message[]>([
        {role: "assistant", content: "Yo. I’m connected to your backend."},
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const inFlight = useRef(false)

    async function sendMessage(e: React.FormEvent) {
        e.preventDefault()
        const text = input.trim()
        if (!text || loading) return

        setInput("")
        setLoading(true)
        inFlight.current = true

        const nextMessages: Message[] = [...messages, {role: "user", content: text}]
        setMessages(nextMessages)

        try {
            const res = await fetch(`${api_base}/api/v1/llm/agent`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    conversation: nextMessages,
                    model_type: "openai",
                    thinking_level: "thinking_on_a_budget"
                }),
            })


            if (!res.ok) throw new Error(`Backend error: ${res.status}`)

            const apiResponse = await res.json() as APIResponse
            setMessages(apiResponse.data)
        } catch (err: any) {
            setMessages([
                ...nextMessages,
                {role: "assistant", content: `Error: ${err.message}`},
            ])
        } finally {
            setLoading(false)
            inFlight.current = false
        }
    }

    return (
        <main className="chat-container">
            <h1 className="chat-title">Osu Agent</h1>

            <div className="chat-box">
                {messages.map((m, i) => (
                    <div key={i} className={`message ${m.role}`}>
                        <div className="message-role">{m.role}</div>
                        {m.content}
                    </div>
                ))}
            </div>

            <form className="chat-form" onSubmit={sendMessage}>
                <input
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button className="chat-button" disabled={loading}>
                    {loading ? "..." : "Send"}
                </button>
            </form>
        </main>
    )
}
