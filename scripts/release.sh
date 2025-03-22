#!/bin/bash

# Obtém a última tag semântica
LAST_TAG=$(git tag --sort=-v:refname | head -n 1)

# Se não houver tags, define a versão inicial
if [[ -z "$LAST_TAG" ]]; then
    LAST_TAG="0.1.0"
fi

echo "Última tag: $LAST_TAG"

# Obtém o número da versão semântica (MAJOR.MINOR.PATCH)
IFS='.' read -r MAJOR MINOR PATCH <<< "$LAST_TAG"

# Verifica os commits desde a última tag
NEW_MAJOR=$(git log "$LAST_TAG"..HEAD --grep="^BREAKING CHANGE" --oneline | wc -l)
NEW_MINOR=$(git log "$LAST_TAG"..HEAD --grep="^feat:" --oneline | wc -l)
NEW_PATCH=$(git log "$LAST_TAG"..HEAD --grep="^fix:" --oneline | wc -l)

# Define a nova versão com base nos commits
if [[ "$NEW_MAJOR" -gt 0 ]]; then
    ((MAJOR++))
    MINOR=0
    PATCH=0
elif [[ "$NEW_MINOR" -gt 0 ]]; then
    ((MINOR++))
    PATCH=0
elif [[ "$NEW_PATCH" -gt 0 ]]; then
    ((PATCH++))
else
    echo "Nenhum commit relevante encontrado. Mantendo a versão atual."
    exit 0
fi

NEW_TAG="$MAJOR.$MINOR.$PATCH"
echo "Nova tag: $NEW_TAG"

# Cria a nova tag
git tag "$NEW_TAG"
git push origin "$NEW_TAG"

# Gera o changelog separado por tags
echo "Atualizando CHANGELOG.md..."
echo -e "\n## $NEW_TAG" >> CHANGELOG.md
git log "$LAST_TAG"..HEAD --pretty=format:"- %s (%h)" --grep="^feat:\|^fix:" >> CHANGELOG.md

# Commit e push do changelog atualizado
git add CHANGELOG.md
git commit -m "docs: Atualiza CHANGELOG para versão $NEW_TAG"
git push origin HEAD