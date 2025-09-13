

export const platformIcons = {
  Messenger: "/channelIcons/telegram.png",
  Instagram: "/channelIcons/instagram.png",
  Telegram: "/channelIcons/telegram.png",
  WhatsApp: "/channelIcons/whatsapp.png",
};


export const users= {
  status: "success",
  data: [
    {
      user_id: "123456789",
      platform: "Messenger",
      name: "John Doe",
      username: "john_doe",
      profile_picture_url: "/images/luffy.jpeg",
      last_interaction_timestamp: "2024-11-25T12:34:56",
    },
    {
      user_id: "987654321",
      platform: "Instagram",
      name: "Jane Smith",
      username: "jane_smith",
      profile_picture_url: "/images/naruto.jpeg",
      last_interaction_timestamp: "2024-11-24T08:15:42",
    },
  ],
  pagination: {
    current_page: 1,
    limit: 10,
    total_users: 25,
    has_next: true,
  },
};

export const ChatData= {
  status: "success",
  data: [
    {
      id: "MSG-001",
      message_id: "mid.123456789",
      from: "123456789", //john
      to: "987654321", //jane smith
      content: {
        text: "Hello friend are you free today?",
        type: "text",
        attachments: [],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: null,
      reply: null,
      referral: null,
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Incoming",
        timestamp: "2024-11-25 12:34:56",
      },
    },
    {
      id: "MSG-002",
      message_id: "mid.987654321",
      from: "987654321",
      to: "123456789",
      content: {
        text: "I am not free I have some task in pending I need to wrap them up soon.",
        type: "text",
        attachments: [
          {
            url: "/private/files/image_attachment.jpg",
            type: "image",
          },
        ],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: {
        emoji: "👍",
        text: "like",
      },
      reply: {
        is_reply: true,
        reply_to: "mid.123456789",
      },
      referral: {
        is_referral: true,
        ref: "some-ref",
        source: "ADS",
        type: "OPEN_THREAD",
        ad_id: "123-ad-id",
        referrer_url: "https://referrer.example.com",
      },
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Outgoing",
        timestamp: "2024-11-25 12:33:45",
      },
    },
    {
      id: "MSG-003",
      message_id: "mid.987654322",
      from: "123456789",
      to: "987654321",
      content: {
        text: "Ok, fine then let's meet at night",
        type: "text",
        attachments: [
          {
            url: "/private/files/image_attachment.jpg",
            type: "image",
          },
        ],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: {
        emoji: "👍",
        text: "like",
      },
      reply: null,
      referral: {
        is_referral: true,
        ref: "some-ref",
        source: "ADS",
        type: "OPEN_THREAD",
        ad_id: "123-ad-id",
        referrer_url: "https://referrer.example.com",
      },
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Incoming",
        timestamp: "2024-11-25 12:35:45",
      },
    },
    {
      id: "MSG-004",
      message_id: "mid.987654323",
      from: "123456789",
      to: "987654321",
      content: {
        text: "Watch this video it's amzing, give your points on this video.",
        type: "video",
        attachments: [
          {
            url: "/videos/vid1.mp4",
            type: "video",
          },
        ],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: {
        emoji: "🤩",
        text: "like",
      },
      reply: null,
      referral: {
        is_referral: true,
        ref: "some-ref",
        source: "ADS",
        type: "OPEN_THREAD",
        ad_id: "123-ad-id",
        referrer_url: "https://referrer.example.com",
      },
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Incoming",
        timestamp: "2024-11-26 12:38:45",
      },
    },
    {
      id: "MSG-005",
      message_id: "mid.987654324",
      from: "987654321",
      to: "123456789",
      content: {
        text: "Listen this audio it's amzing....",
        type: "audio",
        attachments: [
          {
            url: "/audios/aud1.mp3",
            type: "audio",
          },
        ],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: {
        emoji: "🥱",
        text: "like",
      },
      reply: null,
      referral: {
        is_referral: true,
        ref: "some-ref",
        source: "ADS",
        type: "OPEN_THREAD",
        ad_id: "123-ad-id",
        referrer_url: "https://referrer.example.com",
      },
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Outgoing",
        timestamp: "2024-11-26 12:40:45",
      },
    },
    {
      id: "MSG-006",
      message_id: "mid.9876543266",
      from: "123456789",
      to: "987654321",
      content: {
        text: "How is this image....",
        type: "image",
        attachments: [
          {
            url: "/images/img1.jpg",
            type: "image",
          },
        ],
        products: [],
        fallbacks: [],
        reels: [],
      },
      reaction: {
        emoji: "🥱",
        text: "like",
      },
      reply: null,
      referral: {
        is_referral: true,
        ref: "some-ref",
        source: "ADS",
        type: "OPEN_THREAD",
        ad_id: "123-ad-id",
        referrer_url: "https://referrer.example.com",
      },
      quick_reply: null,
      metadata: {
        platform: "Messenger",
        page_id: "987654321",
        status: "Received",
        flow: "Incoming",
        timestamp: "2024-11-26 12:40:45",
      },
    },
  ],
  pagination: {
    current_page: 1,
    limit: 10,
    total_messages: 25,
    has_next: true,
  },
};
