<script>
  import { onDestroy, onMount } from 'svelte';
  import { fetchEmojiLeaderboard, fetchEmojis } from '$lib/services/emojis.js';
  import LeaderboardItem from '$lib/components/LeaderboardItem.svelte';

  let loadInterval = null;
  let emojis = {};
  let leaderboard = {};

  const load = async () => {
    [emojis, leaderboard] = await Promise.all([fetchEmojis(), fetchEmojiLeaderboard()]);
  };

  onMount(() => {
    load();
    loadInterval = setInterval(load, 5000);
  });

  onDestroy(() => clearInterval(loadInterval));
</script>

<svelte:head>
  <title>Emoji Leaderboard</title>
</svelte:head>

<div class="flex h-screen justify-center items-center">
  <table class="flex flex-col space-y-3 w-2/3 lg:w-2/5">
    {#each [...Object.entries(leaderboard).entries()] as [idx, [emoji, uses]] (emoji)}
      <LeaderboardItem
        emoji={[emoji, ...emojis[emoji].aliases].join('/')}
        iconUrl={emojis[emoji].url}
        position={idx}
        {uses}
      />
    {/each}
  </table>
</div>
