module.exports = {
    branches: ['master', 'dev'], // Defina as branches para o release
    plugins: [
      '@semantic-release/commit-analyzer',
      '@semantic-release/release-notes-generator',
      '@semantic-release/changelog',
      '@semantic-release/github',
      '@semantic-release/git',
    ],
};  