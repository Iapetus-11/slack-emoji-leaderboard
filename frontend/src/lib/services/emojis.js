import { env } from '$env/dynamic/public';

/**
 * @returns {Promise<{ emojis: Object<string, Object> }>}
 */
export const fetchEmojis = () => {
  return fetch(`${env.PUBLIC_API_ADDRESS}/emojis/`, {
    headers: { Authorization: env.PUBLIC_API_AUTH },
  }).then((response) => response.json());
};

/**
 * @param {boolean} unique Whether or not duplicate emojis in messages are counted
 * @returns {Promise<Object<string, number>>}
 */
export const fetchEmojiLeaderboard = (unique = false) => {
  return fetch(`${env.PUBLIC_API_ADDRESS}/emojis/leaderboard/?unique=${unique}`, {
    headers: { Authorization: env.PUBLIC_API_AUTH },
  }).then((response) => response.json());
};
