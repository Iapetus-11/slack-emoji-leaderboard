import { PUBLIC_API_ADDRESS, PUBLIC_API_AUTH } from '$env/static/public';

/**
 * @returns {Promise<{ emojis: Object<string, Object> }>}
 */
export const fetchEmojis = () => {
  return fetch(`${PUBLIC_API_ADDRESS}/emojis/`, {
    headers: { Authorization: PUBLIC_API_AUTH },
  }).then((response) => response.json());
};

/**
 * @param {boolean} unique Whether or not duplicate emojis in messages are counted
 * @returns {Promise<Object<string, number>>}
 */
export const fetchEmojiLeaderboard = (unique = true) => {
  return fetch(`${PUBLIC_API_ADDRESS}/emojis/leaderboard/?unique=${unique}`, {
    headers: { Authorization: PUBLIC_API_AUTH },
  }).then((response) => response.json());
};
