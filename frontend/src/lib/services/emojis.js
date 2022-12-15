import { PUBLIC_API_ADDRESS, PUBLIC_API_AUTH } from '$env/static/public';

/**
 * @returns {Promise<{ emojis: Object<string, Object> }>}
 */
export const fetchEmojis = () => {
  return fetch(`${PUBLIC_API_ADDRESS}/emojis/`, {
    headers: { Authorization: PUBLIC_API_AUTH },
  }).then((response) => response.json());
};

export const fetchEmojiLeaderboard = () => {
  return fetch(`${PUBLIC_API_ADDRESS}/emojis/leaderboard/`, {
    headers: { Authorization: PUBLIC_API_AUTH },
  }).then((response) => response.json());
};
