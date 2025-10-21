function write_metadata(meta)
  local function stringify(val)
    return pandoc.utils.stringify(val)
  end

  local function stringify_array(arr)
    local out = {}
    for _, item in ipairs(arr) do
      table.insert(out, stringify(item))
    end
    return out
  end

  local function get_multilingual(base, langs)
    local out = {}
    local fallback = meta[base] and stringify(meta[base]) or nil
    for _, lang in ipairs(langs) do
      if meta[base .. "-" .. lang] then
        out[lang] = stringify(meta[base .. "-" .. lang])
      elseif meta[base .. "Multilingual"] and meta[base .. "Multilingual"][lang] then
        out[lang] = stringify(meta[base .. "Multilingual"][lang])
      elseif fallback then
        out[lang] = fallback
      end
    end
    return out
  end

  local function extract_urls(deployment)
    local result = {}
    for _, item in ipairs(deployment) do
      for platform, val in pairs(item) do
        result[platform] = result[platform] or {}

        if type(val) == "table" then
          local is_lang_map = true
          for _, entry in ipairs(val) do
            if type(entry) ~= "table" then
              is_lang_map = false
              break
            end
          end

          if is_lang_map then
            for _, entry in ipairs(val) do
              for lang, url in pairs(entry) do
                result[platform][lang] = stringify(url)
              end
            end
          else
            result[platform] = stringify_array(val)
          end
        elseif type(val) == "string" then
          result[platform] = { default = stringify(val) }
        end
      end
    end
    return result
  end

  local function get_last_git_commit_date(filepath)
    local cmd = string.format("git log -1 --format=%%cs -- %q", filepath)
    local handle = io.popen(cmd)
    if handle then
      local result = handle:read("*a")
      handle:close()
      result = result:gsub("%s+", "")
      return result ~= "" and result or nil
    end
    return nil
  end

  -- Fix duration if given as a string
  local duration = 0
  if meta.duration then
    local dur_str = stringify(meta.duration)
    duration = tonumber(dur_str) or 0
  end

  -- Authors as flat list of names
  local authors = {}
  if meta.author and type(meta.author) == "table" then
    for _, author in ipairs(meta.author) do
      if author.t == "MetaMap" and author.name then
        table.insert(authors, stringify(author.name))
      else
        table.insert(authors, stringify(author))
      end
    end
  end

  -- Build metadata
  local metadata = {
    name = get_multilingual("title", {"fr", "en"}),
    abstract = get_multilingual("description", {"fr", "en"}),
    authors = authors,
    tags = meta.tags and stringify_array(meta.tags) or {},
    skills = meta.skills and stringify_array(meta.skills) or {},
    timeRequired = duration,
    imageUrl = meta.image and stringify(meta.image) or nil,
    license = meta.license and stringify(meta.license) or nil,
    category = "training courses with R and Python",
    deploymentUrl = meta.deploymentURL and extract_urls(meta.deploymentURL) or {},
    suggestedRequirements = meta.suggestedRequirements and stringify_array(meta.suggestedRequirements) or {},
    lastModification = get_last_git_commit_date(quarto.doc.input_file)
  }

  -- Write to JSON
  local json = pandoc.json.encode(metadata, { indent = true })
  local file = io.open("metadata.json", "w")
  file:write(json)
  file:close()
end

return {
  Meta = write_metadata
}
