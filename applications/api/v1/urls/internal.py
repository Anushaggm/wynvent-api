# coding=utf-8

from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from applications.api.v1 import accounts as account_view
from applications.api.v1 import builders as builder_view
from applications.api.v1 import agents as agent_view
from applications.api.v1 import blogs as blog_view
from applications.api.v1 import properties as property_views
from applications.api.v1 import locations as location_views
from applications.api.v1 import contact_us as contact_views
from applications.api.v1 import feedback as feedback_views
from applications.api.v1 import payment as payment_views
from applications.api.v1 import talk_to_experts as talk_to_experts_views



from utils.decorators import check_authorized

router = DefaultRouter()

urlpatterns = [

    url(r'^login/$', account_view.UserLoginView.as_view(), name='user-login'),

    # Register including social registration
    url(r'^register/$', account_view.UserEmailRegisterView.as_view(), name='user-email-register'),
    url(r'^logout/$', check_authorized(account_view.UserLogoutView.as_view()), name='user-logout'),
    url(r'^check-if-email-exists/$', account_view.CheckIfEmailExistsView.as_view(), name='check-if-email-exists'),
    url(r'^session-status/$', account_view.UserSessionStatusView.as_view(), name='user-session-status'),
    url(r'^account/$', check_authorized(account_view.UserProfileDetail.as_view()), name='user-profile'),
    url(r'^reset-password/$', account_view.PasswordResetView.as_view(), name='user-password-reset'),
    url(r'^reset-password/confirm/$', account_view.PasswordResetConfirmView.as_view(),
        name='user-password-reset-confirm'
        ),
    url(r'^change-password/$', account_view.PasswordChangeView.as_view(), name='user-password-change'),
    url(r'^account/update-profile-image/$', check_authorized(account_view.UpdateUserImage.as_view()),
        name='user-image-update'),
    url(r'^verify-otp/$', account_view.UserOtpVerification.as_view(), name='check-if-otp-verified'),

    # Social Login
    url(r'^login/facebook/$', account_view.FacebookLoginOrSignup.as_view(), name='user-facebook-login-signup'),
    url(r'^login/google/$', account_view.GoogleLogin.as_view(), name='user-google-login-signup'),

    # Property
    url(r'^property/list/$', property_views.PropertyListView.as_view(), name='property-list'),
    url(r'^property/(?P<pk>[0-9]+)/$', property_views.PropertyDetailView.as_view(), name='property-detail'),
    url(r'^property/submit/$', property_views.SubmitPropertyView.as_view(), name='submit-property'),
    url(r'^property/search/$', property_views.PropertySearchView.as_view(), name='property-search'),
    url(r'^property/my-listings/$', property_views.MyPropertyListingsView.as_view(), name='my-property-listings'),
    url(r'^property/responses/$', property_views.PropertyResponsesView.as_view(), name='property-responses'),
    url(r'^property/shortlisted/$', property_views.ShortlistedPropertiesView.as_view(), name='shortlisted-properties'),
    url(r'^facility-types/$', property_views.FacilityTypeListView.as_view(), name='facility-types'),
    url(r'^property/report/$', property_views.PropertyReportView.as_view(), name='property-report'),

    # Builder
    url(r'^builder/$', builder_view.BuilderListView.as_view(), name='builder-list'),
    url(r'^builder/(?P<pk>[0-9]+)/$', builder_view.BuilderDetailView.as_view(), name='builder-detail'),

    # Agent
    url(r'^agent/$', agent_view.AgentListView.as_view(), name='agent-list'),
    url(r'^agent/(?P<pk>[0-9]+)/$', agent_view.AgentDetailView.as_view(), name='agent-detail'),
    url(r'^agent/responses/$', agent_view.AgentResponseListView.as_view(), name='agent-response-list'),

    # Blog
    # url(r'^blog/$', blog_view.BlogListView.as_view(), name='blog-list'),
    # url(r'^blog/(?P<pk>[0-9]+)/$', blog_view.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^blog/$', blog_view.ZinniaListView.as_view(), name='zinnia-list'),
    url(r'^blog/(?P<id>[0-9]+)/$', blog_view.ZinniaDetailView.as_view(), name='zinnia-detail'),
    url(r'^blog-categories/$', blog_view.ZinniaCategorys.as_view(), name='zinnia-categories'),
    url(r'^blog-by-category/(?P<id>[0-9]+)/$', blog_view.BlogList.as_view(), name='zinnia-blogs'),

    #payment
    url(r'^payment/$', payment_views.PaymentExecuteView.as_view(), name='payment'),
    url(r'^payment/go/$', payment_views.PaymentStartView.as_view(), name='payment-start'),

    # Others
    url(r'^cities/$', location_views.CityListView.as_view(), name='cities'),
    url(r'^localities/$', location_views.LocalityListView.as_view(), name='localities'),
    url(r'^contact-us/$', contact_views.ContactListView.as_view(), name='contact-us'),
    url(r'^feedback/$', feedback_views.FeedbackListView.as_view(), name='feedback'),
    url(r'^talk-to-expert/$', talk_to_experts_views.TalkToExpertsListView.as_view(), name='talk-to-expert'),
    url(r'^connect-to-experts/$', talk_to_experts_views.ListExperts.as_view(), name='connect-to-experts'),
    url(r'^get-location-coordinates/$', location_views.LocationPoints.as_view(), name='get-location'),
    url(r'^get-nearest-city/$', location_views.NearestCityView.as_view(), name='get-nearest-city'),
    url(r'^get-locality-detail/$', location_views.GetLocalityDetail.as_view(), name='get-locality-detail'),
    # Advertisement
    url(r'^advertisement/$', property_views.AdvertisementListView.as_view(), name='advertisement-listing'),
    url(r'^banners/$', property_views.BannerListView.as_view(), name='banner-listing'),
    url(r'^activity-based-popup/$', property_views.ActivityListView.as_view(), name='activity-listing'),
    url(r'^user-timer-popup/$', property_views.UserTimerView.as_view(), name='user-timer-popup'),

    # Newsletter
    url(r'^subscribe-newsletter/$', account_view.SubscribeToNewsletterView.as_view(), name='subscribe-newsletter'),

    url(r'^', include(router.urls)),
]
