const PROXY_CONFIG = [
    {
        context: [
            "/cob"
        ],
        target: "http://localhost:8127",
        secure: false,
        logLevel: "debug"
    }
]

module.exports = PROXY_CONFIG;