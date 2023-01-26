<script>
  import { onDestroy, onMount } from 'svelte';
  import { fetchEmojiLeaderboard, fetchEmojis } from '$lib/services/emojis.js';
  import Leaderboard from '$lib/components/Leaderboard.svelte';

  export let data;

  let emojis = {};
  let leaderboard = {};
  let loadInterval = null;

  const load = async () => {
    [emojis, leaderboard] = await Promise.all([fetchEmojis(), fetchEmojiLeaderboard(data.unique)]);
  };

  onMount(() => {
    load();
    loadInterval = setInterval(load, 10000);
  });

  onDestroy(() => clearInterval(loadInterval));
</script>

<svelte:head>
  <title>Emoji Leaderboard</title>
  <link rel="icon" type="image/x-icon" href={emojis[Object.entries(leaderboard)[0]?.[0]]?.url} />
</svelte:head>

<div
  class="flex flex-col h-full items-center p-3 space-y-5
         {data.limit <= 10 ? 'lg:justify-center' : ''}"
>
  <Leaderboard {emojis} {leaderboard} limit={data.limit} />

  <p class="text-gray-500 text-center text-xs mx-5 w-full sm:w-4/5 md:w-3/5 lg:w-2/5">
    This leaderboard is for the past one week of activity (rolling). Both an emoji in a message and
    a reaction to a message constitute a "use".
  </p>
</div>
