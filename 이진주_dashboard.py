
# 라이브러리 불러오기 

import pandas as pd
import streamlit as st
import numpy as np
import datetime
import plotly.express as px


# -------------------- ▼ 필요 변수 생성 코딩 Start ▼ --------------------

data = pd.read_csv('./119_emergency_dispatch.csv', encoding="cp949")

## 오늘 날짜
now_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
now_date2 = datetime.datetime.strptime(now_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

## 2023년 최소 날짜, 최대 날짜
first_date = pd.to_datetime("2023-01-01")
last_date = pd.to_datetime("2023-12-31")

## 출동 이력의 최소 날짜, 최대 날짜
min_date = datetime.datetime.strptime(data['출동일시'].min(), "%Y-%m-%d")
max_date = datetime.datetime.strptime(data['출동일시'].max(), "%Y-%m-%d")


# -------------------- ▲ 필요 변수 생성 코딩 End ▲ --------------------


# -------------------- ▼ Streamlit 웹 화면 구성 START ▼ --------------------

# 레이아웃 구성하기 
st.set_page_config(
    page_title="미니프로젝트 5차",
    page_icon=":bar_chart:",
    layout="wide"
)

# tabs 만들기 
tab1, tab2 = st.tabs(["출동 일지", "대시보드"])
with tab1:
    st.markdown("어제자 실습")
with tab2:
    st.markdown("대시 보드")

    
# tab2 내용 구성하기
 
    
    ## -------------------- ▼ 2-0그룹 금일 출동 이력 출력 ▼ --------------------
    
    st.info('금일 출동 내역')
    
    today_date = now_date.strftime("%Y-%m-%d")
    today_count = len(data[data['출동일시'] == today_date])
    
    if today_count > 0 :
        st.dataframe(data[data['출동일시'] == today_date])
    else:
        st.markdown("금일 출동내역이 없습니다.")
    
    ## -------------------------------------------------------------------

    ## -------------------- ▼ 2-1그룹 통계 조회 기간 선택하기 ▼ --------------------
    col210, col211, col212 = st.columns(3)
    
    with col210:
        slider_date = st.slider('날짜', 
                                min_value=min_date,
                                max_value=max_date,
                                value=(min_date, now_date2))
    with col211:
        slider_week = st.slider('주간', 
                                min_value=min_date,
                                max_value=max_date,
                                step=datetime.timedelta(weeks=1),
                                value=(min_date, now_date2))
    with col212:
        slider_month = st.slider('월간', 
                                min_value=min_date,
                                max_value=max_date,
                                step=datetime.timedelta(weeks=1),
                                value=(min_date, now_date2),
                                format='YYYY-MM')

    ## 선택된 일자의 data 추출
    data['datetime'] = pd.to_datetime(data['출동일시'])
    day_list_df = data[(data['datetime'] >= slider_date[0]) & (data['datetime'] <= slider_date[1])]


    ## 선택된 주간의 data 추출
    
    data['주별'] = data['datetime'].dt.strftime("%W").astype(int)
    
    min_week = int(slider_week[0].strftime("%W"))
    max_week = int(slider_week[1].strftime("%W"))
    week_list_df = data[(data['주별'] >= min_week) & (data['주별'] <= max_week)]
        

    ## 선택된 월의 data 추출
    
    data['월별'] = data['datetime'].dt.month.astype(int)
    min_month = slider_month[0].month
    max_month = slider_month[1].month
    
    month_list_df = data[(data['월별'] >= min_month) & (data['월별'] <= max_month)]


    ## -------------------------------------------------------------------------------------------

    ## -------------------- ▼ 2-2그룹 일간/주간/월간 평균 이송시간 통계 그래프 ▼ --------------------
    

    
    st.success("이송시간 통계")

    col230, col231, col232 = st.columns(3)
    with col230:

        group_day_time = data.groupby(by=['출동일시'], as_index=False)['이송 시간'].mean()
        group_day_time = group_day_time.rename(columns={'이송 시간': '이송 시간'})
        st.line_chart(data=group_day_time, x='출동일시', y='이송 시간', use_container_width=True)

    with col231:
        group_week_time = data.groupby(by=['나이'], as_index=False)['이송 시간'].mean()
        group_week_time = group_week_time.rename(columns={'이송 시간': '이송 시간'})
        st.line_chart(data=group_week_time, x='나이', y='이송 시간', use_container_width=True)

    with col232:
        group_month_time = data.groupby(by=['중증질환'], as_index=False)['이송 시간'].mean()
        group_month_time = group_month_time.rename(columns={'이송 시간': '이송 시간'})
        st.line_chart(data=group_month_time, x='중증질환', y='이송 시간', use_container_width=True)

        
    
    ## -------------------------------------------------------------------------------------------

    ## -------------------- ▼ 2-3 그룹 일간/주간/월간 총 출동 건수 통계 그래프 ▼ --------------------

    
    select_bins = st.radio("주기", ('일별', '주별', '월별'), horizontal=True)
    if select_bins == '일별':
        select_df = day_list_df
    elif select_bins=='주별':
        select_df = week_list_df
    else:
        select_df = month_list_df
    

    st.error("출동 건수")
    
    re_select_df = select_df.rename(columns={"출동일시": '일별'}) 
    dispatch_count = re_select_df.groupby(by=select_bins, as_index=False)['ID'].count()
    dispatch_count = dispatch_count.rename(columns={'ID':'출동건수'})
    dispatch_count = dispatch_count.sort_values(select_bins, ascending=True)

    st.bar_chart(data=dispatch_count, x=select_bins, y='출동건수', use_container_width=True)


    ## -------------------------------------------------------------------------------------------

    ## -------------------- ▼ 2-4 성별/중증질환/나이대 별 비율 그래프 ▼ --------------------
    
    
    st.warning("중증 질환별 통계")

    col240, col241, col242 = st.columns(3)
    
    with col240: # 성별 통계

        group_day_disease = select_df.groupby(by=['성별'], as_index=False)['ID'].count()
        group_day_disease = group_day_disease.rename(columns={'ID':'출동건수'})

        fig = px.pie(group_day_disease, values='출동건수', names='성별', title='성별 통계', hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(font=dict(size=16))
        st.plotly_chart(fig)
      

    with col241: # 중증질환별 통계

        group_day_disease = select_df.groupby(by=['중증질환'], as_index=False)['ID'].count()
        group_day_disease = group_day_disease.rename(columns={'ID':'출동건수'})

        fig = px.pie(group_day_disease, values='출동건수', names='중증질환', title='중증질환별 통계', hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(font=dict(size=16))
        st.plotly_chart(fig)

    with col242:  # 나이대별 통계

        select_df['나이대'] = (select_df['나이']//10)*10
        group_day_disease = select_df.groupby(by=['나이대'], as_index=False)['ID'].count()
        group_day_disease = group_day_disease.rename(columns={'ID':'출동건수'})

        fig = px.pie(group_day_disease, values='출동건수', names='나이대', title='나이대별 통계', hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(font=dict(size=16))
        st.plotly_chart(fig)
    
    ## -------------------------------------------------------------------------------------------

    ## -------------------- ▼ 2-4그룹 그외 필요하다고 생각되는 정보 추가 ▼ --------------------

    
        
