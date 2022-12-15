import { env } from '$env/dynamic/public';

/**
 * @returns {Promise<{ emojis: Object<string, Object> }>}
 */
export const fetchEmojis = () => {
  return fetch(`${env.PUBLIC_API_ADDRESS}/emojis/`, {
    headers: { Authorization: env.PUBLIC_API_AUTH },
  }).then((response) => response.json());
};

export const fetchEmojiLeaderboard = () => {
  return fetch(`${env.PUBLIC_API_ADDRESS}/emojis/leaderboard/`, {
    headers: { Authorization: env.PUBLIC_API_AUTH },
  }).then((response) => response.json());
};
