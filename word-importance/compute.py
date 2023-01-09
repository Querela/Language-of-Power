import collections
import itertools
import logging
import os
import os.path
import pickle
import re

import numpy as np
import pandas as pd
import scipy.sparse
import sklearn.feature_extraction.text
import sklearn.linear_model
import sklearn.preprocessing
import spacy
import matplotlib.pyplot as plt


fn_study1_data = "Study 1/Data Study 1.xlsx"
fn_study2_data = "Study 2/Data Study 2.xlsx"


LOGGER = logging.getLogger(__name__)


# --------------------------------------------------------------------------


def load_study1(fn_data=fn_study1_data):
    df_study1 = pd.read_excel(fn_data)

    # just keep useful columns
    df_study1 = df_study1[
        [
            # id
            "ID",
            # raw text
            "SourceB",
            # other meta
            "Alter",
            "Geschlecht",
            # self-evaluation (mean)
            "Power_mean",
            "Dom_mean",
            "Pres_mean",
            # outside-evaluation (mean)
            "Power_F",
            "Dom_F",
            "Pres_F",
        ]
    ]

    # rename columns
    df_study1.rename(
        columns={
            "SourceB": "text",
            "Alter": "age",
            "Geschlecht": "gender",
            "Power_mean": "power",
            "Dom_mean": "dominance",
            "Pres_mean": "prestige",
            "Power_F": "power_f",
            "Dom_F": "dominance_f",
            "Pres_F": "prestige_f",
        },
        inplace=True,
    )

    return df_study1


def load_study2(fn_data=fn_study2_data):
    df_study2 = pd.read_excel(fn_data)

    # just keep useful columns
    df_study2 = df_study2[
        [
            # id
            "ID",
            # raw text
            "SourceA",
            # other meta
            "Alter",
            "Geschlecht",
            # self-evaluation (mean)
            "Power_means",
            "Dominanz_means",
            "Prestige_means",
            # outside-evaluation (mean)
            "Power_Fremdgesamt_means",
            "Dominanz_Fremdgesamt_means",
            "Prestige_Fremdgesamt_means",
            # WP (workplace power)?
            "WP_means",
            "WP_Fremdgesamt_means",
        ]
    ]

    # rename columns
    df_study2.rename(
        columns={
            "SourceA": "text",
            "Alter": "age",
            "Geschlecht": "gender",
            "Power_means": "power",
            "Dominanz_means": "dominance",
            "Prestige_means": "prestige",
            "Power_Fremdgesamt_means": "power_f",
            "Dominanz_Fremdgesamt_means": "dominance_f",
            "Prestige_Fremdgesamt_means": "prestige_f",
            "WP_means": "workplace_power",
            "WP_Fremdgesamt_means": "workplace_power_f",
        },
        inplace=True,
    )

    return df_study2


# --------------------------------------------------------------------------


def nlpize(df, nlp_fn):
    return df.map(nlp_fn)


# --------------------------------------------------------------------------


def clean(df, stopwords=False, alpha=False, punctuation=True):
    # filter out stopwords
    if stopwords:
        df = df.map(lambda doc: list(filter(lambda tok: not tok.is_stop, doc)))

    # filter alphanumerical
    if alpha:
        df = df.map(lambda doc: list(filter(lambda tok: tok.is_alpha, doc)))

    # filter out punctuation
    if punctuation:
        df = df.map(
            lambda doc: list(filter(lambda tok: tok.pos_ not in ("PUNCT"), doc))
        )

    # filter out space
    df = df.map(lambda doc: list(filter(lambda tok: not tok.is_space, doc)))

    return df


def remove_punct(df):
    return df.map(lambda x: re.sub(r"[,\.!?]", "", x))


def lowercase_text(df):
    return df.map(lambda x: x.lower())


def get_text_by_pos(df, pos_list=("NOUN",), lemma=False, join=True):
    # filter each token by correct pos tag
    if pos_list:
        df = df.map(lambda x: list(filter(lambda tok: tok.pos_ in pos_list, x)))

    # convert tokens back to strings
    # df = df.map(lambda x: " ".join(map(str, x)))
    if lemma:
        df = df.map(lambda x: " ".join(map(lambda tok: tok.lemma_, x)))
    else:
        df = df.map(lambda x: " ".join(map(lambda tok: tok.text, x)))

    # concat to single text
    if not join:
        return df

    return " ".join(df.values.tolist())


def get_tokens_by_pos(df, pos_list=("NOUN",), lemma=False, join=True):
    # filter each token by correct pos tag
    if pos_list:
        df = df.map(lambda x: list(filter(lambda tok: tok.pos_ in pos_list, x)))

    # convert tokens back to strings
    # df = df.map(lambda x: " ".join(map(str, x)))
    if lemma:
        df = df.map(lambda x: list(map(lambda tok: tok.lemma_, x)))
    else:
        df = df.map(lambda x: list(map(lambda tok: tok.text, x)))

    # concat to single text
    if not join:
        return df

    return list(itertools.chain(*df.values.tolist()))


# --------------------------------------------------------------------------


def prepare_study_data():
    LOGGER.info("Load study data ...")
    df_study1 = load_study1()
    df_study2 = load_study2()

    # --------------------------------------------------
    LOGGER.info("Run spaCy on data ...")
    # import de_core_news_sm
    # import de_dep_news_trf
    # nlp = de_core_news_sm.load()
    # nlp = de_dep_news_trf.load()

    # nlp = spacy.load("de_core_news_sm")
    nlp = spacy.load("de_dep_news_trf")

    df_study1["text_spacy_doc"] = nlpize(df_study1["text"], nlp)
    df_study2["text_spacy_doc"] = nlpize(df_study2["text"], nlp)

    # --------------------------------------------------
    return df_study1, df_study2


def clean_study_data(
    df_study1, df_study2, do_clean_stopwords=True, do_clean_alpha=True
):
    LOGGER.info("Clean study data ...")
    df_study1["text_spacy_doc_filtered"] = clean(
        df_study1["text_spacy_doc"],
        stopwords=do_clean_stopwords,
        alpha=do_clean_alpha,
        punctuation=True,
    )
    df_study2["text_spacy_doc_filtered"] = clean(
        df_study2["text_spacy_doc"],
        stopwords=do_clean_stopwords,
        alpha=do_clean_alpha,
        punctuation=True,
    )

    # take raw text `tok.text` instead of lemma `tok.lemma_`
    # df_study1["tokens"] = df_study1["text_spacy_doc_filtered"].map(lambda doc: list(map(lambda tok: tok.text, doc)))
    # df_study2["tokens"] = df_study2["text_spacy_doc_filtered"].map(lambda doc: list(map(lambda tok: tok.text, doc)))
    # convert to plain string
    # df_study1["tokens"] = df_study1["tokens"].map(lambda doc: list(map(str, doc)))
    # df_study2["tokens"] = df_study2["tokens"].map(lambda doc: list(map(str, doc)))

    # Remove punctuation
    # df_study1["text_processed"] = remove_punct(df_study1["text"])
    # df_study2["text_processed"] = remove_punct(df_study2["text"])
    # Convert the titles to lowercase
    # df_study1['text_processed'] = lowercase_text(df_study1['text_processed'])
    # df_study2['text_processed'] = lowercase_text(df_study2['text_processed'])

    # --------------------------------------------------
    return df_study1, df_study2


def load_cached_data(fn_study_prepared="studydata.pickle"):
    if not os.path.exists(fn_study_prepared):
        df_study1, df_study2 = prepare_study_data()

        with open(fn_study_prepared, "wb") as fp:
            pickle.dump(df_study1, fp, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(df_study2, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open(fn_study_prepared, "rb") as fp:
        df_study1 = pickle.load(fp)
        df_study2 = pickle.load(fp)

    df_study1, df_study2 = clean_study_data(df_study1, df_study2)

    return df_study1, df_study2


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


def make_word_freq_df(
    df,
    by="power",
    pos=("NOUN", "PROPN"),
    lemma=True,
    max_freq=None,
    min_freq=10,
    relative=False,
):
    row = df[by].map(round)

    dfs_score = []
    for score in range(1, 8):  # range: [1, 7]
        mask = row == score
        df_sub = df[mask]["text_spacy_doc_filtered"]
        tokens = get_tokens_by_pos(df_sub, pos_list=pos, lemma=lemma, join=True)
        cnt = collections.Counter(tokens)

        df_score = pd.DataFrame.from_dict(cnt, orient="index").rename(
            columns={0: f"{by}={score}"}
        )
        dfs_score.append(df_score)

    df_scores = pd.concat(dfs_score, axis=1).fillna(0)
    df_scores["_total"] = df_scores.sum(axis=1)
    df_scores = df_scores.sort_values("_total", ascending=False)
    if max_freq is not None:
        df_scores = df_scores[df_scores["_total"] <= max_freq]
    if min_freq is not None:
        df_scores = df_scores[df_scores["_total"] >= min_freq]
    del df_scores["_total"]

    if relative:
        totals = df_scores.sum(axis=0)
        df_scores /= totals

    return df_scores


def make_word_freq_score_comparison_df(
    df,
    parts,
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=None,
):
    dfs_cnts = []
    for mask, name in parts:
        df_sub = df[mask]["text_spacy_doc_filtered"]
        tokens_low = get_tokens_by_pos(df_sub, pos_list=pos, lemma=lemma, join=True)
        cnt = collections.Counter(tokens_low)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "Top words: %s",
                "".join(
                    ["{} ({})".format(w, n) for w, n in cnt.most_common(10) if n > 1]
                ),
            )
        df_cnt = pd.DataFrame.from_dict(cnt, orient="index").rename(
            columns={0: name}
        )  # .reset_index()
        dfs_cnts.append(df_cnt)

    df_lmh = pd.concat(dfs_cnts, axis=1).fillna(0)
    df_lmh["_total"] = df_lmh.sum(axis=1)
    df_lmh = df_lmh.sort_values("_total", ascending=False)
    df_lmh = df_lmh[df_lmh["_total"] >= total_occ_min]
    del df_lmh["_total"]

    # restrict to max N entries
    if max_rows is not None and max_rows > 0:
        df_lmh = df_lmh.head(max_rows)

    if relative:
        # make relative
        totals = df_lmh.sum(axis=0)
        df_lmh /= totals

    return df_lmh


def make_word_freq_score_lmh_comparison_df(
    df,
    what,
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=20,
):
    parts = list(zip(get_lmh_quantiles_mask(df, what), ["low", "mid", "high"]))

    return make_word_freq_score_comparison_df(
        df,
        parts,
        pos=pos,
        lemma=lemma,
        relative=relative,
        total_occ_min=total_occ_min,
        max_rows=max_rows,
    )


def make_word_freq_score_pdp_comparison_df(
    df,
    whats=("power", "dominance", "prestige"),
    range_=(2 / 3, 1.0),
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=20,
):
    parts = []
    for what in whats:
        q1, q2 = df[what].quantile(range_)
        if range_[0] <= 0.0:
            mask = df[what] <= q2
        elif range_[1] >= 1.0:
            mask = df[what] > q1
        else:
            mask = (df[what] > q1) & (df[what] <= q2)
        parts.append([mask, what.title()])

    return make_word_freq_score_comparison_df(
        df,
        parts,
        pos=pos,
        lemma=lemma,
        relative=relative,
        total_occ_min=total_occ_min,
        max_rows=max_rows,
    )


def get_lmh_quantiles_mask(df, what):
    q33 = df[what].quantile(1 / 3)
    q66 = df[what].quantile(2 / 3)

    mask_low = df[what] <= q33
    mask_mid = (df[what] > q33) & (df[what] <= q66)
    mask_high = df[what] > q66

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug("quant(%s): low: %s", what, len(df[mask_low]))
        LOGGER.debug("quant(%s): mid: %s", what, len(df[mask_mid]))
        LOGGER.debug("quant(%s): high: %s", what, len(df[mask_high]))

    return mask_low, mask_mid, mask_high


# --------------------------------------------------------------------------


def write_freqs_to_excel(
    df_study, fn_output="output.xlsx", lemma=True, relative=False, total_occ_min=3
):
    with pd.ExcelWriter(fn_output) as writer:
        df_study_t = df_study.copy()
        df_study_t = df_study_t[list(set(df_study.columns) - {"text_spacy_doc"})]
        df_study_t["text_spacy_doc_filtered"] = df_study_t[
            "text_spacy_doc_filtered"
        ].map(lambda x: ", ".join(map(lambda tok: tok.text, x)))
        df_study_t.to_excel(writer, sheet_name="Study Data")

        pdp = ["power", "dominance", "prestige"]
        pdpf = ["power_f", "dominance_f", "prestige_f"]
        if "workplace_power" in df_study.columns:
            pdp += ["workplace_power"]
            pdpf += ["workplace_power_f"]

        df_study_quants = df_study[pdp + pdpf].quantile([0 / 3, 1 / 3, 2 / 3, 3 / 3])
        df_study_quants.to_excel(writer, sheet_name="Quantiles")

        # by trait, for POS tags, per low/mid/high
        poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
        for pos in poss:
            for what in pdp:
                df_lmh = make_word_freq_score_lmh_comparison_df(
                    df_study,
                    what,
                    pos=pos,
                    lemma=lemma,
                    relative=relative,
                    total_occ_min=total_occ_min,
                )
                title = "Words for '{}' for {}".format(
                    what.replace("workplace_power", "WrkPow")
                    .replace("dominance", "Dom")
                    .title(),
                    ", ".join(pos),
                )
                df_lmh.to_excel(writer, sheet_name=title[10:].replace("'", ""))

        # by quantil range + per category/dimension/trait
        poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
        ranges = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
        whatss = [pdp, pdpf, *zip(pdp, pdpf)]
        for pos in poss:
            for range_ in ranges:
                for wi, whats in enumerate(whatss):
                    df_h_pdp = make_word_freq_score_pdp_comparison_df(
                        df_study,
                        whats=whats,
                        range_=range_,
                        pos=pos,
                        lemma=lemma,
                        relative=relative,
                        total_occ_min=total_occ_min,
                    )
                    title = "Words for quantile {:.2f}-{:.2f} for {}".format(
                        *range_, ", ".join(pos)
                    )
                    title = "Qnt {:.1f}-{:.1f} for {} {}".format(
                        *range_, ",".join(pos), wi
                    )
                    df_h_pdp.to_excel(writer, sheet_name=title)


def generate_freqs_figures(
    df_study,
    dn_output="figures",
    lemma=True,
    relative=True,
    total_occ_min=10,
    max_rows=20,
    plot_type="barh",
):
    os.makedirs(dn_output, exist_ok=True)
    os.makedirs(os.path.join(dn_output, "distribution"), exist_ok=True)
    os.makedirs(os.path.join(dn_output, "mid-low-high"), exist_ok=True)
    os.makedirs(os.path.join(dn_output, "comparison"), exist_ok=True)

    pdp = ["power", "dominance", "prestige"]
    pdpf = ["power_f", "dominance_f", "prestige_f"]
    if "workplace_power" in df_study.columns:
        pdp += ["workplace_power"]
        pdpf += ["workplace_power_f"]

    for what in pdp + pdpf:
        df_study[what].hist()
        min_ylim, max_ylim = plt.ylim()
        q33 = df_study[what].quantile(1 / 3)
        q66 = df_study[what].quantile(2 / 3)
        plt.axvline(q33, color="k", linestyle="dashed", linewidth=1)
        plt.text(q33 * 1.01, max_ylim * 0.9, "{:.2f}".format(q33))
        plt.axvline(q66, color="k", linestyle="dashed", linewidth=1)
        plt.text(q66 * 1.01, max_ylim * 0.9, "{:.2f}".format(q66))
        plt.savefig(
            os.path.join(
                dn_output, "distribution", "quant-{}.png".format(what.lower())
            ),
            bbox_inches="tight",
        )
        plt.close()

    # by trait, for POS tags, per low/mid/high
    poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
    for pos in poss:
        for what in pdp:
            local_total_occ_min = total_occ_min
            if pos in (("ADJ",),):
                local_total_occ_min = 3
            df_lmh = make_word_freq_score_lmh_comparison_df(
                df_study,
                what,
                pos=pos,
                lemma=lemma,
                relative=relative,
                total_occ_min=local_total_occ_min,
                max_rows=max_rows,
            )
            title = "Words for '{}' for {}".format(what.title(), ", ".join(pos))
            df_lmh.plot(kind=plot_type)
            plt.title(title)
            plt.savefig(
                os.path.join(
                    dn_output,
                    "mid-low-high",
                    "words-{}-by-pos-{}.png".format(what.lower(), ",".join(pos)),
                ),
                bbox_inches="tight",
            )
            plt.close()

    # by quantil range + per category/dimension/trait
    poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
    ranges = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
    whatss = [pdp, pdpf, *zip(pdp, pdpf)]
    for pos in poss:
        for range_ in ranges:
            for whats in whatss:
                local_total_occ_min = total_occ_min
                if pos in (("ADJ",),):
                    local_total_occ_min = 3
                df_h_pdp = make_word_freq_score_pdp_comparison_df(
                    df_study,
                    whats=whats,
                    range_=range_,
                    pos=pos,
                    lemma=lemma,
                    relative=relative,
                    total_occ_min=local_total_occ_min,
                    max_rows=max_rows,
                )
                title = "Words for quantile {:.2f}-{:.2f} for {}".format(
                    *range_, ", ".join(pos)
                )
                df_h_pdp.plot(kind=plot_type)
                plt.title(title)
                plt.savefig(
                    os.path.join(
                        dn_output,
                        "comparison",
                        "words-by-quant-{:.1f}-{:.1f}+pos-{}-for-{}.png".format(
                            *range_, ",".join(pos), ",".join(whats)
                        ),
                    ),
                    bbox_inches="tight",
                )
                plt.close()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------


def build_count_matrix(df, pos_list=None, lemma=False):
    # tokens
    df_tokens = get_tokens_by_pos(df, pos_list=pos_list, lemma=lemma, join=False)
    # token counts
    df_tokens_cnt = df_tokens.map(lambda x: collections.Counter(x))
    # aggregate count --> features
    cnt_tokens = collections.Counter()
    df_tokens_cnt.map(cnt_tokens.update)

    # features
    features = list(cnt_tokens.keys())

    # build sparse features matrix (document, term)
    indptr = [0]
    indices = []
    values = []
    for row in df_tokens_cnt:
        for term, num in row.items():
            indices.append(features.index(term))
            values.append(num)
        indptr.append(len(indices))

    doc_term_mat = scipy.sparse.csr_array((values, indices, indptr), dtype=int)
    # for sklearn `features_names_in_`
    doc_term_mat.columns = features

    return doc_term_mat, features


def build_feature_matrix(df, pos_list=None, lemma=False, norm="l1", use_idf=False):
    transformer = sklearn.feature_extraction.text.TfidfTransformer(
        norm=norm, use_idf=use_idf
    )

    doc_term_mat, features = build_count_matrix(df, pos_list=pos_list, lemma=lemma)

    doc_term_mat = transformer.fit_transform(doc_term_mat.toarray())
    # for sklearn `features_names_in_`
    doc_term_mat.columns = features

    return doc_term_mat, features


# --------------------------------------------------------------------------


def train_prepare(df_study, pos_list=None, lemma=False):
    df_sub = df_study["text_spacy_doc_filtered"]
    # doc_term_mat, features = build_count_matrix(df_sub, pos_list=pos_list, lemma=lemma)
    doc_term_mat, features = build_feature_matrix(
        df_sub, pos_list=pos_list, lemma=lemma, norm="l2", use_idf=True
    )

    return doc_term_mat


def train_model(df_study, what, doc_term_mat):
    # if doc_term_mat is None:
    #     doc_term_mat = train_prepare(df_study)

    clf = sklearn.linear_model.LogisticRegression()

    X = doc_term_mat
    y = df_study[what].to_numpy()

    # classification
    # y = y.astype(int)
    # y = np.vectorize(round)(y)
    y = y.round()

    # regression: to interval [0, 1]
    # y = (y - np.min(y)) / np.ptp(y)
    # y = y[:,np.newaxis]

    # train model
    clf.fit(X, y)
    LOGGER.info("score (on train): %s (for '%s')", clf.score(X, y), what)

    return clf


def coef_aggregate(coefs, num_classes):
    coefs = coefs * np.linspace(-1, 1, num_classes)[:, np.newaxis]
    return coefs.sum(axis=0)


def normalize_coefs(coefs, neg_coefs=True):
    if neg_coefs:
        # norm: [-1, 1]
        coefs = 2.0 * (coefs - np.min(coefs)) / np.ptp(coefs) - 1
    else:
        # norm: [0, 1]
        coefs = (coefs - np.min(coefs)) / np.ptp(coefs)

    return coefs


def coef_filter(coef, features, min_threshold=0.25, max_features=20, require_both=True):
    if require_both:
        # try to request from both ends to keep pos and neg (min/max)
        mask = np.zeros_like(coef).astype(bool)
        mask[: max_features // 2 + 1] = mask[-max_features // 2 :] = True

        srt = np.argsort(coef)[::-1]
        # pre-filter features
        features = np.array(features)[srt][mask]
        coef = np.array(coef)[srt][mask]

    # sort by importance (most positive/negative first)
    srt = np.argsort(np.abs(coef))[::-1]
    # minimum importance filter
    mask = np.abs(coef) >= min_threshold
    mask_srt = mask[srt]
    # max feature filter
    mask_srt[max_features:] = False
    # filter features
    labels_srt = np.array(features)[srt][mask_srt]
    values_srt = np.array(coef)[srt][mask_srt]

    # sort by value descending
    srt = np.argsort(values_srt)[::-1]
    labels = labels_srt[srt]
    values = values_srt[srt]

    return values, labels


def coef_to_human(values, labels):
    return " + ".join(
        "{:.2f}*'{}'".format(value, label) for label, value in zip(labels, values)
    )


# --------------------------------------------------------------------------


def write_coefs_to_excel(
    clf,
    what,
    fn_output="coefs.xlsx",
    min_threshold=0.20,
    max_features=30,
    require_both=False,
):
    skip = 4
    features = clf.feature_names_in_
    coefs = clf.coef_.copy()
    coefs = normalize_coefs(coefs)

    mode = "a" if os.path.exists(fn_output) else "w"
    ise = "overlay" if os.path.exists(fn_output) else None
    with pd.ExcelWriter(fn_output, mode=mode, if_sheet_exists=ise) as writer:
        # per class coefs
        for ci, (class_, coef) in enumerate(zip(clf.classes_, coefs)):
            values, labels = coef_filter(
                coef,
                features,
                min_threshold=min_threshold,
                max_features=max_features,
                require_both=require_both,
            )
            col_lbl = "Class {:d}".format(int(class_))
            cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
            df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
            df_coef.to_excel(
                writer, sheet_name="{}".format(what.title()), startcol=ci * skip
            )

        ci += 1
        # aggregated coefs
        coefs = clf.coef_.copy()
        coefs = coefs * np.linspace(-1, 1, len(clf.classes_))[:, np.newaxis]
        coefs = coefs.sum(axis=0)
        coefs = normalize_coefs(coefs)
        values, labels = coef_filter(
            coefs,
            features,
            min_threshold=min_threshold,
            max_features=max_features,
            require_both=require_both,
        )
        col_lbl = "Aggregated"
        cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
        df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
        df_coef.to_excel(
            writer, sheet_name="{}".format(what.title()), startcol=ci * skip
        )

        # averaged coedfs
        # should not make sense as we then have equal contributions from both low and high power for example
        # ci += 1
        # coefs = clf.coef_.copy()
        # coefs = coefs.mean(axis=0)
        # coefs = normalize_coefs(coefs)
        # values, labels = coef_filter(coefs, features, min_threshold=min_threshold, max_features=max_features, require_both=require_both)
        # col_lbl = "Averaged"
        # cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
        # df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
        # df_coef.to_excel(writer, sheet_name="{}".format(what.title()), startcol=ci*3)


def train_and_write_coefs_to_excel(
    df_study,
    fn_output="coefs.xlsx",
    pos_list=None,
    lemma=False,
    min_threshold=0.20,
    max_features=30,
    require_both=True,
):
    pdp = ["power", "dominance", "prestige"]
    pdpf = ["power_f", "dominance_f", "prestige_f"]
    if "workplace_power" in df_study.columns:
        pdp += ["workplace_power"]
        pdpf += ["workplace_power_f"]

    doc_term_mat = train_prepare(df_study, pos_list=pos_list, lemma=lemma)
    for what in pdp + pdpf:
        clf = train_model(df_study, what, doc_term_mat=doc_term_mat)
        write_coefs_to_excel(
            clf,
            what,
            fn_output=fn_output,
            min_threshold=min_threshold,
            max_features=max_features,
            require_both=require_both,
        )


# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s"
    )
    LOGGER.info("Run as script ...")

    LOGGER.info("Load data ...")
    df_study1, df_study2 = load_cached_data()

    LOGGER.info("Write Excel data ...")
    write_freqs_to_excel(df_study1, "study1-output.xlsx")
    write_freqs_to_excel(df_study2, "study2-output.xlsx")

    LOGGER.info("Generate figures ...")
    generate_freqs_figures(df_study1, "figures_study1")
    generate_freqs_figures(df_study2, "figures_study2")

    LOGGER.info("Compute word importance ...")
    train_and_write_coefs_to_excel(df_study1, "study1-coefs.xlsx")
    train_and_write_coefs_to_excel(df_study2, "study2-coefs.xlsx")
    train_and_write_coefs_to_excel(df_study1, "study1-coefs-lemma.xlsx", lemma=True)
    train_and_write_coefs_to_excel(df_study2, "study2-coefs-lemma.xlsx", lemma=True)

    LOGGER.info("Done.")


# --------------------------------------------------------------------------
