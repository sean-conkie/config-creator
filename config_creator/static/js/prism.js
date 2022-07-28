/* PrismJS 1.28.0
https://prismjs.com/download.html#themes=prism&languages=sql */
const _self = typeof window !== 'undefined' ? window : typeof WorkerGlobalScope !== 'undefined' && self instanceof WorkerGlobalScope ? self : {} // eslint-disable-line no-undef
const Prism = (function (e) {
  const n = /(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i
  let t = 0
  const r = {}
  const a = {
    manual: e.Prism && e.Prism.manual,
    disableWorkerMessageHandler: e.Prism && e.Prism.disableWorkerMessageHandler,
    util: {
      encode: function e (n) {
        return n instanceof i ? new i(n.type, e(n.content), n.alias) : Array.isArray(n) ? n.map(e) : n.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\u00a0/g, ' ') // eslint-disable-line new-cap
      },
      type: function (e) {
        return Object.prototype.toString.call(e).slice(8, -1)
      },
      objId: function (e) {
        return e.__id || Object.defineProperty(e, '__id', {
          value: ++t
        }), e.__id // eslint-disable-line no-sequences
      },
      clone: function e (n, t) {
        let r, i
        switch (t = t || {}, a.util.type(n)) { // eslint-disable-line no-sequences
          case 'Object':
            if (i = a.util.objId(n), t[i]) return t[i] // eslint-disable-line no-sequences
            for (const l in r = {}, t[i] = r, n) n.hasOwnProperty(l) && (r[l] = e(n[l], t)) // eslint-disable-line no-sequences, no-prototype-builtins
            return r
          case 'Array':
            return i = a.util.objId(n), t[i] // eslint-disable-line no-return-assign, no-sequences
              ? t[i]
              : (r = [], t[i] = r, n.forEach(function (n, a) {
                  r[a] = e(n, t)
                }), r)
          default:
            return n
        }
      },
      getLanguage: function (e) {
        for (; e;) {
          const t = n.exec(e.className)
          if (t) return t[1].toLowerCase()
          e = e.parentElement
        }
        return 'none'
      },
      setLanguage: function (e, t) {
        e.className = e.className.replace(RegExp(n, 'gi'), ''), e.classList.add('language-' + t) // eslint-disable-line no-unused-expressions, no-sequences
      },
      currentScript: function () {
        if (typeof document === 'undefined') return null
        if ('currentScript' in document) return document.currentScript
        try {
          throw new Error()
        } catch (r) {
          const e = (/at [^(\r\n]*\((.*):[^:]+:[^:]+\)$/i.exec(r.stack) || [])[1]
          if (e) {
            const n = document.getElementsByTagName('script')
            for (const t in n) { if (n[t].src === e) return n[t] }
          }
          return null
        }
      },
      isActive: function (e, n, t) {
        for (let r = 'no-' + n; e;) {
          const a = e.classList
          if (a.contains(n)) return !0
          if (a.contains(r)) return !1
          e = e.parentElement
        }
        return !!t
      }
    },
    languages: {
      plain: r,
      plaintext: r,
      text: r,
      txt: r,
      extend: function (e, n) {
        const t = a.util.clone(a.languages[e])
        for (const r in n) t[r] = n[r]
        return t
      },
      insertBefore: function (e, n, t, r) {
        const i = (r = r || a.languages)[e]
        const l = {}
        for (const o in i) {
          if (i.hasOwnProperty(o)) { // eslint-disable-line no-prototype-builtins
            if (o === n) { for (const s in t) t.hasOwnProperty(s) && (l[s] = t[s]) } // eslint-disable-line no-prototype-builtins
            t.hasOwnProperty(o) || (l[o] = i[o]) // eslint-disable-line no-prototype-builtins
          }
        } const u = r[e]
        return r[e] = l, a.languages.DFS(a.languages, function (n, t) { // eslint-disable-line no-return-assign, no-sequences
          t === u && n !== e && (this[n] = l)
        }), l
      },
      DFS: function e (n, t, r, i) {
        i = i || {}
        const l = a.util.objId
        for (const o in n) {
          if (n.hasOwnProperty(o)) { // eslint-disable-line no-prototype-builtins
            t.call(n, o, n[o], r || o)
            const s = n[o]
            const u = a.util.type(s)
            u !== 'Object' || i[l(s)] ? u !== 'Array' || i[l(s)] || (i[l(s)] = !0, e(s, t, o, i)) : (i[l(s)] = !0, e(s, t, null, i)) // eslint-disable-line no-unused-expressions
          }
        }
      }
    },
    plugins: {},
    highlightAll: function (e, n) {
      a.highlightAllUnder(document, e, n)
    },
    highlightAllUnder: function (e, n, t) {
      const r = {
        callback: t,
        container: e,
        selector: 'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'
      }
      a.hooks.run('before-highlightall', r), r.elements = Array.prototype.slice.apply(r.container.querySelectorAll(r.selector)), a.hooks.run('before-all-elements-highlight', r) // eslint-disable-line no-unused-expressions, no-sequences
      for (let i, l = 0; i = r.elements[l++];) a.highlightElement(i, !0 === n, r.callback) // eslint-disable-line no-cond-assign
    },
    highlightElement: function (n, t, r) {
      const i = a.util.getLanguage(n)
      const l = a.languages[i]
      a.util.setLanguage(n, i)
      let o = n.parentElement
      o && o.nodeName.toLowerCase() === 'pre' && a.util.setLanguage(o, i)
      const s = {
        element: n,
        language: i,
        grammar: l,
        code: n.textContent
      }

      function u (e) {
        s.highlightedCode = e, a.hooks.run('before-insert', s), s.element.innerHTML = s.highlightedCode, a.hooks.run('after-highlight', s), a.hooks.run('complete', s), r && r.call(s.element) // eslint-disable-line no-unused-expressions, no-sequences
      }
      if (a.hooks.run('before-sanity-check', s), (o = s.element.parentElement) && o.nodeName.toLowerCase() === 'pre' && !o.hasAttribute('tabindex') && o.setAttribute('tabindex', '0'), !s.code) return a.hooks.run('complete', s), void (r && r.call(s.element)) // eslint-disable-line no-sequences, no-void
      if (a.hooks.run('before-highlight', s), s.grammar) { // eslint-disable-line no-sequences
        if (t && e.Worker) {
          const c = new Worker(a.filename) // eslint-disable-line no-undef
          c.onmessage = function (e) { // eslint-disable-line no-unused-expressions
            u(e.data)
          }, c.postMessage(JSON.stringify({ // eslint-disable-line no-sequences
            language: s.language,
            code: s.code,
            immediateClose: !0
          }))
        } else u(a.highlight(s.code, s.grammar, s.language))
      } else u(a.util.encode(s.code))
    },
    highlight: function (e, n, t) {
      const r = {
        code: e,
        grammar: n,
        language: t
      }
      if (a.hooks.run('before-tokenize', r), !r.grammar) throw new Error('The language "' + r.language + '" has no grammar.') // eslint-disable-line no-sequences
      return r.tokens = a.tokenize(r.code, r.grammar), a.hooks.run('after-tokenize', r), i.stringify(a.util.encode(r.tokens), r.language) // eslint-disable-line no-sequences, no-cond-assign, no-return-assign
    },
    tokenize: function (e, n) {
      const t = n.rest
      if (t) {
        for (const r in t) n[r] = t[r]
        delete n.rest
      }
      const a = new s() // eslint-disable-line new-cap
      return u(a, a.head, e), o(e, a, n, a.head, 0), (function (e) { // eslint-disable-line no-sequences
        for (let n = [], t = e.head.next; t !== e.tail;) n.push(t.value), t = t.next // eslint-disable-line no-unused-expressions, no-sequences
        return n
      }(a))
    },
    hooks: {
      all: {},
      add: function (e, n) {
        const t = a.hooks.all
        t[e] = t[e] || [], t[e].push(n) // eslint-disable-line no-unused-expressions, no-sequences
      },
      run: function (e, n) {
        const t = a.hooks.all[e]
        if (t && t.length) { for (let r, i = 0; r = t[i++];) r(n) } // eslint-disable-line no-cond-assign
      }
    },
    Token: i
  }

  function i (e, n, t, r) {
    this.type = e, this.content = n, this.alias = t, this.length = 0 | (r || '').length // eslint-disable-line no-unused-expressions, no-sequences
  }

  function l (e, n, t, r) {
    e.lastIndex = n
    const a = e.exec(t)
    if (a && r && a[1]) {
      const i = a[1].length
      a.index += i, a[0] = a[0].slice(i) // eslint-disable-line no-unused-expressions, no-sequences
    }
    return a
  }

  function o (e, n, t, r, s, g) {
    for (const f in t) {
      if (t.hasOwnProperty(f) && t[f]) { // eslint-disable-line no-prototype-builtins
        let h = t[f]
        h = Array.isArray(h) ? h : [h]
        for (let d = 0; d < h.length; ++d) {
          if (g && g.cause === f + ',' + d) return
          const v = h[d]
          const p = v.inside
          const m = !!v.lookbehind
          const y = !!v.greedy
          const k = v.alias
          if (y && !v.pattern.global) {
            const x = v.pattern.toString().match(/[imsuy]*$/)[0]
            v.pattern = RegExp(v.pattern.source, x + 'g')
          }
          for (let b = v.pattern || v, w = r.next, A = s; w !== n.tail && !(g && A >= g.reach); A += w.value.length, w = w.next) { // eslint-disable-line no-unmodified-loop-condition
            let E = w.value
            if (n.length > e.length) return
            if (!(E instanceof i)) {
              let P
              let L = 1
              if (y) {
                if (!(P = l(b, A, e, m)) || P.index >= e.length) break
                const S = P.index
                const O = P.index + P[0].length
                let j = A
                for (j += w.value.length; S >= j;) j += (w = w.next).value.length
                if (A = j -= w.value.length, w.value instanceof i) continue // eslint-disable-line no-sequences
                for (let C = w; C !== n.tail && (j < O || typeof C.value === 'string'); C = C.next) L++, j += C.value.length // eslint-disable-line no-unused-expressions, no-sequences
                L--, E = e.slice(A, j), P.index -= A // eslint-disable-line no-unused-expressions, no-sequences
              } else if (!(P = l(b, 0, E, m))) continue
              S = P.index // eslint-disable-line no-undef
              const N = P[0]
              const _ = E.slice(0, S) // eslint-disable-line no-undef
              const M = E.slice(S + N.length) // eslint-disable-line no-undef
              const W = A + E.length
              g && W > g.reach && (g.reach = W)
              let z = w.prev
              if (_ && (z = u(n, z, _), A += _.length), c(n, z, L), w = u(n, z, new i(f, p ? a.tokenize(N, p) : N, k, N)), M && u(n, w, M), L > 1) { // eslint-disable-line no-sequences, new-cap
                const I = {
                  cause: f + ',' + d,
                  reach: W
                }
                o(e, n, t, w.prev, A, I), g && I.reach > g.reach && (g.reach = I.reach) // eslint-disable-line no-unused-expressions, no-sequences
              }
            }
          }
        }
      }
    }
  }

  function s () {
    const e = {
      value: null,
      prev: null,
      next: null
    }
    const n = {
      value: null,
      prev: e,
      next: null
    }
    e.next = n, this.head = e, this.tail = n, this.length = 0 // eslint-disable-line no-unused-expressions, no-sequences
  }

  function u (e, n, t) {
    const r = n.next
    const a = {
      value: t,
      prev: n,
      next: r
    }
    return n.next = a, r.prev = a, e.length++, a // eslint-disable-line no-sequences, no-return-assign
  }

  function c (e, n, t) {
    for (let r = n.next, a = 0; a < t && r !== e.tail; a++) r = r.next
    n.next = r, r.prev = n, e.length -= a // eslint-disable-line no-unused-expressions, no-sequences
  }
  if (e.Prism = a, i.stringify = function e (n, t) { // eslint-disable-line no-sequences
    if (typeof n === 'string') return n
    if (Array.isArray(n)) {
      let r = ''
      return n.forEach(function (n) {
        r += e(n, t)
      }), r // eslint-disable-line no-sequences
    }
    const i = {
      type: n.type,
      content: e(n.content, t),
      tag: 'span',
      classes: ['token', n.type],
      attributes: {},
      language: t
    }
    const l = n.alias
    l && (Array.isArray(l) ? Array.prototype.push.apply(i.classes, l) : i.classes.push(l)), a.hooks.run('wrap', i) // eslint-disable-line no-unused-expressions, no-sequences
    let o = ''
    for (const s in i.attributes) o += ' ' + s + '="' + (i.attributes[s] || '').replace(/"/g, '&quot;') + '"'
    return '<' + i.tag + ' class="' + i.classes.join(' ') + '"' + o + '>' + i.content + '</' + i.tag + '>'
  }, !e.document) {
    return e.addEventListener
      ? (a.disableWorkerMessageHandler || e.addEventListener('message', function (n) {
          const t = JSON.parse(n.data)
          const r = t.language
          const i = t.code
          const l = t.immediateClose
          e.postMessage(a.highlight(i, a.languages[r], r)), l && e.close() // eslint-disable-line no-unused-expressions, no-sequences
        }, !1), a)
      : a
  }
  const g = a.util.currentScript()

  function f () {
    a.manual || a.highlightAll()
  }
  if (g && (a.filename = g.src, g.hasAttribute('data-manual') && (a.manual = !0)), !a.manual) { // eslint-disable-line no-sequences
    const h = document.readyState
    h === 'loading' || h === 'interactive' && g && g.defer ? document.addEventListener('DOMContentLoaded', f) : window.requestAnimationFrame ? window.requestAnimationFrame(f) : window.setTimeout(f, 16) // eslint-disable-line no-mixed-operators
  }
  return a
}(_self))
typeof module !== 'undefined' && module.exports && (module.exports = Prism), typeof global !== 'undefined' && (global.Prism = Prism) // eslint-disable-line no-unused-expressions, no-sequences
Prism.languages.sql = {
  comment: {
    pattern: /(^|[^\\])(?:\/\*[\s\S]*?\*\/|(?:--|\/\/|#).*)/,
    lookbehind: !0
  },
  variable: [{
    pattern: /@(["'`])(?:\\[\s\S]|(?!\1)[^\\])+\1/,
    greedy: !0
  }, /@[\w.$]+/],
  string: {
    pattern: /(^|[^@\\])("|')(?:\\[\s\S]|(?!\2)[^\\]|\2\2)*\2/,
    greedy: !0,
    lookbehind: !0
  },
  identifier: {
    pattern: /(^|[^@\\])`(?:\\[\s\S]|[^`\\]|``)*`/,
    greedy: !0,
    lookbehind: !0,
    inside: {
      punctuation: /^`|`$/
    }
  },
  function: /\b(?:AVG|COUNT|FIRST|FORMAT|LAST|LCASE|LEN|MAX|MID|MIN|MOD|NOW|ROUND|SUM|UCASE)(?=\s*\()/i,
  keyword: /\b(?:ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|CALL|CASCADED?|CASE|CHAIN|CHAR(?:ACTER|SET)?|CHECK(?:POINT)?|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMNS?|COMMENT|COMMIT(?:TED)?|COMPUTE|CONNECT|CONSISTENT|CONSTRAINT|CONTAINS(?:TABLE)?|CONTINUE|CONVERT|CREATE|CROSS|CURRENT(?:_DATE|_TIME|_TIMESTAMP|_USER)?|CURSOR|CYCLE|DATA(?:BASES?)?|DATE(?:TIME)?|DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITERS?|DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|DOUBLE|DROP|DUMMY|DUMP(?:FILE)?|DUPLICATE|ELSE(?:IF)?|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|ERRORS|ESCAPED?|EXCEPT|EXEC(?:UTE)?|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR(?: EACH ROW)?|FORCE|FOREIGN|FREETEXT(?:TABLE)?|FROM|FULL|FUNCTION|GEOMETRY(?:COLLECTION)?|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|HOLDLOCK|HOUR|IDENTITY(?:COL|_INSERT)?|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEYS?|KILL|LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONG(?:BLOB|TEXT)|LOOP|MATCH(?:ED)?|MEDIUM(?:BLOB|INT|TEXT)|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|MONTH|MULTI(?:LINESTRING|POINT|POLYGON)|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|NUMERIC|OFF?|OFFSETS?|ON|OPEN(?:DATASOURCE|QUERY|ROWSET)?|OPTIMIZE|OPTION(?:ALLY)?|ORDER|OUT(?:ER|FILE)?|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC(?:EDURE)?|PUBLIC|PURGE|QUICK|RAISERROR|READS?|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT(?:ABLE)?|REPLACE|REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURN(?:ING|S)?|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW(?:COUNT|GUIDCOL|S)?|RTREE|RULE|SAVE(?:POINT)?|SCHEMA|SECOND|SELECT|SERIAL(?:IZABLE)?|SESSION(?:_USER)?|SET(?:USER)?|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|START(?:ING)?|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLES?|TABLESPACE|TEMP(?:ORARY|TABLE)?|TERMINATED|TEXT(?:SIZE)?|THEN|TIME(?:STAMP)?|TINY(?:BLOB|INT|TEXT)|TOP?|TRAN(?:SACTIONS?)?|TRIGGER|TRUNCATE|TSEQUAL|TYPES?|UNBOUNDED|UNCOMMITTED|UNDEFINED|UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE(?:TEXT)?|USAGE|USE|USER|USING|VALUES?|VAR(?:BINARY|CHAR|CHARACTER|YING)|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH(?: ROLLUP|IN)?|WORK|WRITE(?:TEXT)?|YEAR)\b/i,
  boolean: /\b(?:FALSE|NULL|TRUE)\b/i,
  number: /\b0x[\da-f]+\b|\b\d+(?:\.\d*)?|\B\.\d+\b/i,
  operator: /[-+*\/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?|\b(?:AND|BETWEEN|DIV|ILIKE|IN|IS|LIKE|NOT|OR|REGEXP|RLIKE|SOUNDS LIKE|XOR)\b/i, // eslint-disable-line no-useless-escape
  punctuation: /[;[\]()`,.]/
}
